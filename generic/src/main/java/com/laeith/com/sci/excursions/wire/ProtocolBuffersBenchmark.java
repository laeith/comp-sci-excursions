package com.laeith.com.sci.excursions.wire;

import com.google.protobuf.InvalidProtocolBufferException;
import com.google.protobuf.Message;
import com.laeith.com.sci.excursions.utils.StaticData;
import com.laeith.playground.protobuf.messages.Core;
import org.openjdk.jmh.annotations.Benchmark;
import org.openjdk.jmh.annotations.BenchmarkMode;
import org.openjdk.jmh.annotations.Fork;
import org.openjdk.jmh.annotations.Measurement;
import org.openjdk.jmh.annotations.Mode;
import org.openjdk.jmh.annotations.OutputTimeUnit;
import org.openjdk.jmh.annotations.Scope;
import org.openjdk.jmh.annotations.State;
import org.openjdk.jmh.annotations.Warmup;
import org.openjdk.jmh.infra.Blackhole;

import java.io.IOException;
import java.util.concurrent.TimeUnit;

@BenchmarkMode(Mode.Throughput)
@Warmup(iterations = 5, time = 3, timeUnit = TimeUnit.SECONDS)
@Measurement(iterations = 5, time = 3, timeUnit = TimeUnit.SECONDS)
@OutputTimeUnit(TimeUnit.MILLISECONDS)
@Fork(3)
public class ProtocolBuffersBenchmark {
  
  @State(Scope.Benchmark)
  public static class ProtoState {
    byte[] serializedMessage = generateMessage().toByteArray();
  }
  
  @Benchmark
  public byte[] measureSerialization(final ProtoState state) throws IOException {
    return generateMessage().toByteArray();
  }
  
  @Benchmark
  public Message measureDeserialization(final ProtoState state) throws InvalidProtocolBufferException {
    return Core.PingPong.parseFrom(state.serializedMessage);
  }
  
  @Benchmark
  public byte[] measureDeserializeSerialize(final ProtoState state, Blackhole bc) throws InvalidProtocolBufferException {
    Core.PingPong pingPongDeserialized = Core.PingPong.parseFrom(state.serializedMessage);
    
    Core.PingPong newPingPongMsg = Core.PingPong.newBuilder(pingPongDeserialized)
        .setId(-pingPongDeserialized.getId())
        .build();
    
    bc.consume(pingPongDeserialized);
    return newPingPongMsg.toByteArray();
  }
  
  private static Message generateMessage() {
    // Turns out that reusing a single builder is counter-productive for Java client and we get similar performance
    return Core.PingPong.newBuilder()
        .setId(1)
        .setVersion(2)
        .setMessage("Random message - " + System.currentTimeMillis())
        .setIsImportant(true)
        .addAllNames(StaticData.NAMES)
        .addAllInts(StaticData.INTS)
        .addAllDoubles(StaticData.DOUBLES)
        .build();
  }
  
}
