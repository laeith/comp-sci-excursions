package com.laeith.com.sci.excursions.utils;

public class Measure {
  
  /**
   * Returns execution time in nanoseconds
   */
  public static long getExecutionTime(Runnable runnable) {
    long startTimeNano = System.nanoTime();
    
    runnable.run();
    
    return System.nanoTime() - startTimeNano;
  }
  
  public static long fromNsToSeconds(long nanoSeconds) {
    return nanoSeconds / 1_000_000_000;
  }
  
}
