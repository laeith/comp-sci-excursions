package com.laeith.com.sci.excursions.utils.instrumentation;

import org.junit.jupiter.api.Test;

import java.util.stream.IntStream;

class LocalInstrumentationTest {
  
  @Test
  public void toyWithMemoryInstrumentation() {
    LocalInstrumentation.init();
    
    System.out.println("Started instrumentation");
    
    DefaultAllocationSampler.start();
    
    IntStream.range(0, 1).forEach(num -> {
      var testString = new String("Iters: " + num);
      var testClass = new AllocationTestClass();
    });
    
    DefaultAllocationSampler.stop();
    
    System.out.println("Finished");
    
    System.out.println("Implement a pretty summary...");
  }
  
  
}