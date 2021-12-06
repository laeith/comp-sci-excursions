package com.laeith.com.sci.excursions.wire;

import com.laeith.com.sci.excursions.utils.StaticData;
import com.laeith.playground.BooleanType;
import com.laeith.playground.MessageHeaderDecoder;
import com.laeith.playground.MessageHeaderEncoder;
import com.laeith.playground.PingPongDecoder;
import com.laeith.playground.PingPongEncoder;
import org.agrona.concurrent.UnsafeBuffer;
import org.openjdk.jmh.annotations.Benchmark;
import org.openjdk.jmh.annotations.BenchmarkMode;
import org.openjdk.jmh.annotations.Fork;
import org.openjdk.jmh.annotations.Measurement;
import org.openjdk.jmh.annotations.Mode;
import org.openjdk.jmh.annotations.OutputTimeUnit;
import org.openjdk.jmh.annotations.Scope;
import org.openjdk.jmh.annotations.State;
import org.openjdk.jmh.annotations.Warmup;

import java.nio.ByteBuffer;
import java.util.concurrent.TimeUnit;

@BenchmarkMode(Mode.Throughput)
@Warmup(iterations = 5, time = 3, timeUnit = TimeUnit.SECONDS)
@Measurement(iterations = 5, time = 3, timeUnit = TimeUnit.SECONDS)
@OutputTimeUnit(TimeUnit.MILLISECONDS)
@Fork(3)
public class SBEBenchmark {
  
  @State(Scope.Benchmark)
  public static class SBEState {
    final int bufferIndex = 0;
    
    final MessageHeaderEncoder messageHeaderEncoder = new MessageHeaderEncoder();
    final MessageHeaderDecoder messageHeaderDecoder = new MessageHeaderDecoder();
    
    final PingPongEncoder pingPongEncoder = new PingPongEncoder();
    final PingPongDecoder pingPongDecoder = new PingPongDecoder();
    
    final UnsafeBuffer encodingBuffer = new UnsafeBuffer(ByteBuffer.allocate(1024));
    final UnsafeBuffer decodingBuffer = new UnsafeBuffer(ByteBuffer.allocate(1024));
    
    // Encode a ping-pong message for deserialization in benchmarks
    {
      SBEBenchmark.encode(messageHeaderEncoder, pingPongEncoder, decodingBuffer, bufferIndex);
    }
  }
  
  @Benchmark
  public int measureSerialization(final SBEState state) {
    final MessageHeaderEncoder headerEncoder = state.messageHeaderEncoder;
    final PingPongEncoder pingPongEncoder = state.pingPongEncoder;
    final UnsafeBuffer buffer = state.encodingBuffer;
    final int bufferIndex = state.bufferIndex;
    
    encode(headerEncoder, pingPongEncoder, buffer, bufferIndex);
    
    return pingPongEncoder.encodedLength();
  }
  
  @Benchmark
  public int measureDeserialization(final SBEState state) {
    final MessageHeaderDecoder messageHeaderDecoder = state.messageHeaderDecoder;
    final PingPongDecoder pingPongDecoder = state.pingPongDecoder;
    final UnsafeBuffer buffer = state.decodingBuffer;
    final int bufferIndex = state.bufferIndex;
    
    decode(messageHeaderDecoder, pingPongDecoder, buffer, bufferIndex);
    
    return pingPongDecoder.encodedLength();
  }
  
  private static void decode(
      final MessageHeaderDecoder messageHeader,
      final PingPongDecoder pingPongDecoder,
      final UnsafeBuffer buffer,
      final int bufferIndex) {
    messageHeader.wrap(buffer, bufferIndex);
    
    final int currentVersion = messageHeader.version();
    final int blockLen = messageHeader.blockLength();
    
    pingPongDecoder.wrap(buffer, bufferIndex + messageHeader.encodedLength(), blockLen, currentVersion);
    
    //  So, this is the interesting part, technically, we got the data, SBE is a zero-copy approach
    //  but in order to make it comparable we make an attempt at accessing the data
    //  as it is the actual moment when it gets deserialized
    pingPongDecoder.id();
    pingPongDecoder.version();
    pingPongDecoder.message();
    pingPongDecoder.isImportant();
    
    for (PingPongDecoder.NamesDecoder nameEntry : pingPongDecoder.names()) {
      nameEntry.name();
    }
    
    for (PingPongDecoder.IntsDecoder intEntry : pingPongDecoder.ints()) {
      intEntry.record();
    }
    
    for (PingPongDecoder.DoublesDecoder doubleEntry : pingPongDecoder.doubles()) {
      doubleEntry.record();
    }
  }
  
  private static void encode(final MessageHeaderEncoder messageHeader,
                             final PingPongEncoder pingPong,
                             final UnsafeBuffer buffer,
                             final int bufferIndex) {
    pingPong.wrapAndApplyHeader(buffer, bufferIndex, messageHeader)
        .id(1)
        .version(2)
        .isImportant(BooleanType.T)
        .message("Random message - " + System.currentTimeMillis());
    
    final PingPongEncoder.NamesEncoder namesEncoder = pingPong.namesCount(StaticData.NAMES.size());
    StaticData.NAMES.forEach(name -> namesEncoder.next().name(name));
    
    final PingPongEncoder.IntsEncoder intsEncoder = pingPong.intsCount(StaticData.INTS.size());
    StaticData.INTS.forEach(num -> intsEncoder.next().record(num));
    
    final PingPongEncoder.DoublesEncoder doublesEncoder = pingPong.doublesCount(StaticData.DOUBLES.size());
    StaticData.DOUBLES.forEach(num -> doublesEncoder.next().record(num));
  }
  
  
}
