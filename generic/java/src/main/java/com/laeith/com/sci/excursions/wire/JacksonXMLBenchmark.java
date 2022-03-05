package com.laeith.com.sci.excursions.wire;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.dataformat.xml.XmlMapper;
import com.laeith.com.sci.excursions.utils.StaticData;
import com.laeith.com.sci.excursions.wire.json.PingPongJava;
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
public class JacksonXMLBenchmark {
  
  @State(Scope.Benchmark)
  public static class JacksonXMLState {
    XmlMapper xmlMapper = new XmlMapper();
    byte[] serializedXml;
    
    {
      try {
        serializedXml = xmlMapper.writeValueAsBytes(generateMessage());
      } catch (JsonProcessingException e) {
        e.printStackTrace();
      }
    }
  }
  
  @Benchmark
  public byte[] measureSerialization(final JacksonXMLState state) throws JsonProcessingException {
    return state.xmlMapper.writeValueAsBytes(generateMessage());
  }
  
  @Benchmark
  public PingPongJava measureDeserialization(final JacksonXMLState state) throws IOException {
    return state.xmlMapper.readValue(state.serializedXml, PingPongJava.class);
  }
  
  private static PingPongJava generateMessage() {
    PingPongJava pingPong = new PingPongJava();
    pingPong.id = 1;
    pingPong.version = 2;
    pingPong.message = "Random message - " + System.currentTimeMillis();
    pingPong.isImportant = true;
    pingPong.names = StaticData.NAMES;
    pingPong.ints = StaticData.INTS;
    pingPong.doubles = StaticData.DOUBLES;
    
    return pingPong;
  }
}
