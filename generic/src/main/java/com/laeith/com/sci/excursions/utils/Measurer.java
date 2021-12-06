package com.laeith.com.sci.excursions.utils;

import java.util.concurrent.TimeUnit;

public class Measurer {
  
  private int testSize;
  
  public Measurer(int testSize) {
    this.testSize = testSize;
  }
  
  public void measureAndPrintPretty(Runnable runnable, TimeUnit timeUnit) {
    System.out.println("Measuring '" + runnable + "' with test size: " + testSize);
    System.out.println("Task took: " + measure(runnable, timeUnit) + " " + timeUnit.name().toLowerCase() +
        " on average run");
  }
  
  public long measure(Runnable runnable, TimeUnit timeUnit) {
    long startTime = System.currentTimeMillis();
    
    for (int i = 0; i < testSize; i++) {
      runnable.run();
    }
    
    long endTime = System.currentTimeMillis();
    
    switch (timeUnit) {
      case SECONDS:
        return ((endTime - startTime) / testSize) / 1000;
      case MILLISECONDS:
        return ((endTime - startTime) / testSize);
      default:
        throw new IllegalArgumentException("Provided timeunit is not supported yet");
    }
  }
  
}
