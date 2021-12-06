package com.laeith.com.sci.excursions.problems.general;

import java.util.List;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import java.util.stream.Collectors;
import java.util.stream.LongStream;
import java.util.stream.Stream;

public class Fibonacci {
  
  //  Test performance using JMH
  //  1. Memoization
  //  2. Stream parallelization
  
  private static Map<Long, Long> memoizationMap = new ConcurrentHashMap<>();
  
  static List<Long> getFibonacciSequenceRecursively(long n) {
    return LongStream.range(1, n + 1)
        .map(i -> {
          long fib = Fibonacci.getFibNumberRecursively(i);
          memoizationMap.put(i, fib);
          return fib;
        })
        .boxed()
        .collect(Collectors.toList());
  }
  
  private static long getFibNumberRecursively(long n) {
    if (memoizationMap.containsKey(n)) {
      return memoizationMap.get(n);
    }
    if (n < 1) {
      throw new IllegalArgumentException("n must be bigger than 0");
    }
    if (n == 1 || n == 2) {
      return 1;
    }
    return getFibNumberRecursively(n - 1) + getFibNumberRecursively(n - 2);
  }
  
  static String getFibStream(int n) {
    return Stream.iterate(new int[]{0, 1}, t -> new int[]{t[1], t[0] + t[1]})
        .limit(n)
        .map(fib -> String.valueOf(fib[0]))
        .collect(Collectors.joining(", "));
  }
  
}
