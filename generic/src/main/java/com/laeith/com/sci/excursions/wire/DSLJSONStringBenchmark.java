package com.laeith.com.sci.excursions.wire;


import com.dslplatform.json.DslJson;
import com.laeith.com.sci.excursions.utils.StaticData;
import com.laeith.com.sci.excursions.wire.json.PingPongJava;
import com.laeith.com.sci.excursions.wire.json.StringMsg;
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
public class DSLJSONStringBenchmark {
  
  @State(Scope.Benchmark)
  public static class DSLJSONStringState {
    DslJson<PingPongJava> dslJson = new DslJson<>();
    ByteArrayOutputStream outputStream = new ByteArrayOutputStream();
    
    byte[] serializedJson;
    
    {
      try {
        outputStream.reset();
        dslJson.serialize(generateMessage(), outputStream);
        serializedJson = outputStream.toByteArray();
      } catch (IOException e) {
        e.printStackTrace();
      }
    }
  }
  
  @Benchmark
  public byte[] measureSerialization(final DSLJSONStringState state) throws IOException {
    state.outputStream.reset();
    state.dslJson.serialize(generateMessage(), state.outputStream);
    return state.outputStream.toByteArray();
  }
  
  @Benchmark
  public StringMsg measureDeserialization(final DSLJSONStringState state) throws IOException {
    return state.dslJson.deserialize(StringMsg.class, state.serializedJson, state.serializedJson.length);
  }
  
  private static StringMsg generateMessage() {
    StringMsg msg = new StringMsg();
    msg.setStr1(StaticData.REASONABLY_LONG_STRING);
    msg.setStr2(StaticData.REASONABLY_LONG_STRING);
    msg.setStr3(StaticData.REASONABLY_LONG_STRING);
    msg.setStr4(StaticData.REASONABLY_LONG_STRING);
    msg.setStr5(StaticData.REASONABLY_LONG_STRING);
    msg.setStrings(StaticData.NAMES);
    
    return msg;
  }
}
