package com.laeith.com.sci.excursions.funkyjava;

import java.util.List;
import java.util.concurrent.CompletableFuture;
import java.util.stream.Collectors;
import java.util.stream.IntStream;

/**
 * Why does it deadlock?
 * <p>
 * It's unfortunate that parallel streams by default use a ForkJoinPool.commonPool() of threads, the same pool of
 * threads is used to execute async tasks so sooner or later we'll get stuck where all commonPool threads are
 * stuck on waiting for more threads in the same pool.
 */
public class Deadlock2 {
  public static void main(String[] args) {
    List<Integer> items = IntStream.range(0, 50).boxed().collect(Collectors.toList());
    
    // Using ForkJoinPool.commonPool()
    List<Integer> results = items.parallelStream()
        .map(Deadlock2::process)
        .collect(Collectors.toList());
    
    System.out.println(results);
  }
  
  private static Integer process(int x) {
    System.out.println(Thread.currentThread() + " in " + x);
    
    // Again - using ForkJoinPool.commonPool() - see supplyAsync docs.
    CompletableFuture<Integer> async = CompletableFuture.supplyAsync(() -> someAdditionalProcessing(x));
    
    while (!async.isDone()) {
      try {
        Thread.sleep(1);
      } catch (InterruptedException e) {
        e.printStackTrace();
      }
    }
    
    return async.join();
  }
  
  private static int someAdditionalProcessing(int x) {
    return x + 1;
  }
}
