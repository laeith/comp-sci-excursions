package com.laeith.com.sci.excursions.wire;

import com.google.protobuf.InvalidProtocolBufferException;
import com.google.protobuf.Message;
import com.laeith.com.sci.excursions.utils.StaticData;
import com.laeith.com.sci.excursions.wire.json.DoublesOnly;
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

import java.util.concurrent.TimeUnit;

@BenchmarkMode(Mode.Throughput)
@Warmup(iterations = 5, time = 3, timeUnit = TimeUnit.SECONDS)
@Measurement(iterations = 5, time = 3, timeUnit = TimeUnit.SECONDS)
@OutputTimeUnit(TimeUnit.MILLISECONDS)
@Fork(3)
public class ProtocolBuffersDoublesBenchmark {
  
  @State(Scope.Benchmark)
  public static class ProtoDoublesState {
    DoublesOnly doublesOnly = new DoublesOnly();
    byte[] serializedMessage = generateMessage(this).toByteArray();
  }
  
  @Benchmark
  public byte[] measureSerialization(final ProtoDoublesState state) {
    return generateMessage(state).toByteArray();
  }
  
  @Benchmark
  public Message measureDeserialization(final ProtoDoublesState state) throws InvalidProtocolBufferException {
    return Core.DoublesMsg.parseFrom(state.serializedMessage);
  }
  
  private static Message generateMessage(final ProtoDoublesState state) {
    return Core.DoublesMsg.newBuilder()
        .setDouble1(state.doublesOnly.double1)
        .setDouble2(state.doublesOnly.double2)
        .setDouble3(state.doublesOnly.double3)
        .setDouble4(state.doublesOnly.double4)
        .setDouble5(state.doublesOnly.double5)
        .addAllDoubles(StaticData.DOUBLES)
        .build();
  }
}
