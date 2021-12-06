package com.laeith.com.sci.excursions.problems.general;

import org.junit.jupiter.api.Test;
import org.openjdk.jmh.annotations.Benchmark;
import org.openjdk.jmh.annotations.BenchmarkMode;
import org.openjdk.jmh.annotations.Measurement;
import org.openjdk.jmh.annotations.Mode;
import org.openjdk.jmh.annotations.OutputTimeUnit;
import org.openjdk.jmh.annotations.Warmup;

import java.util.concurrent.TimeUnit;

class FibonacciTest {
  
  //  1, 1, 2, 3, 5, 8, 13, 21, 34
  @Test
  void printFibonacci() {
    System.out.println(Fibonacci.getFibonacciSequenceRecursively(100));
  }
  
  @Benchmark
  @BenchmarkMode(Mode.AverageTime)
  @OutputTimeUnit(TimeUnit.MILLISECONDS)
  @Warmup(iterations = 3)
  @Measurement(iterations = 3)
  public void benchmarkFibonacci() {
//    For n = 30
//    Pure recursion - 6.342
//    With memoization - 0.001
//    Parallel - not worth checking...
    Fibonacci.getFibonacciSequenceRecursively(30);
  }
  
}