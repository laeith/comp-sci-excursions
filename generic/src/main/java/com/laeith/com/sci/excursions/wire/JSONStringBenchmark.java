package com.laeith.com.sci.excursions.wire;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.laeith.com.sci.excursions.utils.StaticData;
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

import java.io.IOException;
import java.util.concurrent.TimeUnit;

@BenchmarkMode(Mode.Throughput)
@Warmup(iterations = 5, time = 3, timeUnit = TimeUnit.SECONDS)
@Measurement(iterations = 5, time = 3, timeUnit = TimeUnit.SECONDS)
@OutputTimeUnit(TimeUnit.MILLISECONDS)
@Fork(3)
public class JSONStringBenchmark {
  
  @State(Scope.Benchmark)
  public static class JSONStringState {
    ObjectMapper objectMapper = new ObjectMapper();
    byte[] serializedJson;
    
    {
      try {
        serializedJson = objectMapper.writeValueAsBytes(generateMessage());
      } catch (JsonProcessingException e) {
        e.printStackTrace();
      }
    }
  }
  
  @Benchmark
  public byte[] measureSerialization(final JSONStringState state) throws JsonProcessingException {
    return state.objectMapper.writeValueAsBytes(generateMessage());
  }
  
  @Benchmark
  public StringMsg measureDeserialization(final JSONStringState state) throws IOException {
    return state.objectMapper.readValue(state.serializedJson, StringMsg.class);
  }
  
  public static StringMsg generateMessage() {
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
