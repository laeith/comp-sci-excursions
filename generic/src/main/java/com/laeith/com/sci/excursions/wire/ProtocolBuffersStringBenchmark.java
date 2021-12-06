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

import java.util.concurrent.TimeUnit;

@BenchmarkMode(Mode.Throughput)
@Warmup(iterations = 5, time = 3, timeUnit = TimeUnit.SECONDS)
@Measurement(iterations = 5, time = 3, timeUnit = TimeUnit.SECONDS)
@OutputTimeUnit(TimeUnit.MILLISECONDS)
@Fork(3)
public class ProtocolBuffersStringBenchmark {
  
  @State(Scope.Benchmark)
  public static class ProtoState {
    byte[] serializedMessage = generateMessage().toByteArray();
  }
  
  @Benchmark
  public byte[] measureSerialization() {
    return generateMessage().toByteArray();
  }
  
  @Benchmark
  public Message measureDeserialization(final ProtoState state) throws InvalidProtocolBufferException {
    return Core.StringMsg.parseFrom(state.serializedMessage);
  }
  
  private static Message generateMessage() {
    return Core.StringMsg.newBuilder()
        .setStr1(StaticData.REASONABLY_LONG_STRING)
        .setStr2(StaticData.REASONABLY_LONG_STRING)
        .setStr3(StaticData.REASONABLY_LONG_STRING)
        .setStr4(StaticData.REASONABLY_LONG_STRING)
        .setStr5(StaticData.REASONABLY_LONG_STRING)
        .addAllStrings(StaticData.NAMES)
        .build();
  }
  
}
