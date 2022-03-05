package com.laeith.com.sci.excursions.wire;

import com.laeith.com.sci.excursions.utils.StaticData;
import com.laeith.playground.avro.messages.PingPong;
import org.apache.avro.io.DatumWriter;
import org.apache.avro.io.Encoder;
import org.apache.avro.io.EncoderFactory;
import org.apache.avro.specific.SpecificDatumWriter;
import org.openjdk.jmh.annotations.Benchmark;
import org.openjdk.jmh.annotations.BenchmarkMode;
import org.openjdk.jmh.annotations.Fork;
import org.openjdk.jmh.annotations.Measurement;
import org.openjdk.jmh.annotations.Mode;
import org.openjdk.jmh.annotations.OutputTimeUnit;
import org.openjdk.jmh.annotations.Scope;
import org.openjdk.jmh.annotations.State;
import org.openjdk.jmh.annotations.Warmup;

import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.util.concurrent.TimeUnit;

@BenchmarkMode(Mode.Throughput)
@Warmup(iterations = 5, time = 3, timeUnit = TimeUnit.SECONDS)
@Measurement(iterations = 5, time = 3, timeUnit = TimeUnit.SECONDS)
@OutputTimeUnit(TimeUnit.MILLISECONDS)
@Fork(3)
public class AvroBenchmark {
  
  @State(Scope.Benchmark)
  public static class AvroState {
    PingPong.Builder builder = PingPong.newBuilder();
    
    DatumWriter<PingPong> pingPongWriter = new SpecificDatumWriter<>(PingPong.class);
    ByteArrayOutputStream outputStream = new ByteArrayOutputStream();
    Encoder binaryEncoder = new EncoderFactory().binaryEncoder(outputStream, null);
    
    byte[] serializedMessage;
    
    {
      try {
        serializedMessage = generateMessage(builder).toByteBuffer().array();
      } catch (IOException e) {
        e.printStackTrace();
      }
    }
  }
  
  @Benchmark
  public byte[] measureSerialization(final AvroState state) throws IOException {
    // TODO: Might be possible to avoid data copying / buffer creation - see RawMessageEncoder@copyOutputBytes property
    return generateMessage(state.builder).toByteBuffer().array();
  }
  
  @Benchmark
  public byte[] measureSerializationWithReusableByteBuffer(final AvroState state) throws IOException {
    state.outputStream.reset();
    state.pingPongWriter.write(generateMessage(state.builder), state.binaryEncoder);
    state.binaryEncoder.flush();
    return state.outputStream.toByteArray(); // toByteArray() copies data
  }
  
  @Benchmark
  public PingPong measureDeserialization(final AvroState state) throws IOException {
    return PingPong.getDecoder().decode(state.serializedMessage);
  }
  
  @Benchmark
  public byte[] measureDeserializeSerialize(final AvroState state) throws IOException {
    PingPong decodedPingPongMsg = PingPong.getDecoder().decode(state.serializedMessage);
    
    decodedPingPongMsg.setId(-decodedPingPongMsg.getId());
    
    return decodedPingPongMsg.toByteBuffer().array();
  }
  
  private static PingPong generateMessage(PingPong.Builder builder) {
    return builder
        .clearId()
        .clearVersion()
        .clearMessage()
        .clearIsImportant()
        .clearNames()
        .clearInts()
        .clearDoubles()
        .setId(1)
        .setVersion(2)
        .setMessage("Random message - " + System.currentTimeMillis())
        .setIsImportant(true)
        .setNames(StaticData.NAMES)
        .setInts(StaticData.INTS)
        .setDoubles(StaticData.DOUBLES)
        .build();
  }
}
