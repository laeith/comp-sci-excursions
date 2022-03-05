package com.laeith.com.sci.excursions.optional;

import org.openjdk.jmh.annotations.Benchmark;
import org.openjdk.jmh.annotations.BenchmarkMode;
import org.openjdk.jmh.annotations.Fork;
import org.openjdk.jmh.annotations.Measurement;
import org.openjdk.jmh.annotations.Mode;
import org.openjdk.jmh.annotations.OutputTimeUnit;
import org.openjdk.jmh.annotations.Scope;
import org.openjdk.jmh.annotations.State;
import org.openjdk.jmh.annotations.Warmup;

import java.util.Optional;
import java.util.concurrent.TimeUnit;

/**
 * Attempts to measure different performance implications for different
 * ways of representing 'missing' value in Java.
 */
@State(Scope.Thread)
@Fork(1)
@Warmup(iterations = 2)
@Measurement(iterations = 5)
public class OptionBenchmark {
  
  private static final MutableLong value = new MutableLong();
  
  private long randomNumberWithPrimitives(int n) {
    int i = n % 100;
    if (i > 98) {
      return 0;
    } else {
      return i;
    }
  }
  
  private MutableLong randomNumberWithMutable(int n) {
    int i = n % 100;
    if (i > 98) {
      return null;
    } else {
      return value.set(i);
    }
  }
  
  private Long randomNumber(int n) {
    int i = n % 100;
    if (i > 98) {
      return null;
    } else {
      return (long) i;
    }
  }
  
  private Optional<Long> randomNumberOpt(int n) {
    int i = n % 100;
    if (i > 98) {
      return Optional.empty();
    } else {
      return Optional.of((long) i);
    }
  }
  
  @Benchmark
  @BenchmarkMode(Mode.AverageTime)
  @OutputTimeUnit(TimeUnit.MICROSECONDS)
  public long sumClassicWithMutable() {
    int k = 0;
    long sum = 0;
    for (int i = 0; i < 1_000_000; ++i) {
      MutableLong n = randomNumberWithMutable(k++);
      if (n != null) {
        sum += n.value;
      }
    }
    return sum;
  }
  
  @Benchmark
  @BenchmarkMode(Mode.AverageTime)
  @OutputTimeUnit(TimeUnit.MICROSECONDS)
  public long sumClassicWithPrimitives() {
    int k = 0;
    long sum = 0;
    for (int i = 0; i < 1_000_000; ++i) {
      long n = randomNumberWithPrimitives(k++);
      sum += n;
    }
    return sum;
  }
  
  @Benchmark
  @BenchmarkMode(Mode.AverageTime)
  @OutputTimeUnit(TimeUnit.MICROSECONDS)
  public long sumClassic() {
    int k = 0;
    long sum = 0;
    for (int i = 0; i < 1_000_000; ++i) {
      Long n = randomNumber(k++);
      if (n != null) {
        sum += n;
      }
    }
    return sum;
  }
  
  @Benchmark
  @BenchmarkMode(Mode.AverageTime)
  @OutputTimeUnit(TimeUnit.MICROSECONDS)
  public long sumOptional() {
    int k = 0;
    long sum = 0;
    for (int i = 0; i < 1_000_000; ++i) {
      Optional<Long> n = randomNumberOpt(k++);
      if (n.isPresent()) {
        sum += n.get();
      }
    }
    return sum;
  }
  
}
