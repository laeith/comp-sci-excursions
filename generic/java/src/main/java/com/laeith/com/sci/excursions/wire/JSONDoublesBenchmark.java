package com.laeith.com.sci.excursions.wire;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.laeith.com.sci.excursions.wire.json.DoublesOnly;
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
public class JSONDoublesBenchmark {
  
  @State(Scope.Benchmark)
  public static class JSONDoublesState {
    ObjectMapper objectMapper = new ObjectMapper();
    byte[] serializedJson;
    
    {
      try {
        serializedJson = objectMapper.writeValueAsBytes(new DoublesOnly());
      } catch (JsonProcessingException e) {
        e.printStackTrace();
      }
    }
  }
  
  @Benchmark
  public byte[] measureSerialization(final JSONDoublesState state) throws JsonProcessingException {
    return state.objectMapper.writeValueAsBytes(new DoublesOnly());
  }
  
  @Benchmark
  public DoublesOnly measureDeserialization(final JSONDoublesState state) throws IOException {
    return state.objectMapper.readValue(state.serializedJson, DoublesOnly.class);
  }
  
}
