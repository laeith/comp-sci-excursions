package com.laeith.com.sci.excursions.utils;

import java.util.List;
import java.util.Random;
import java.util.stream.Collectors;
import java.util.stream.IntStream;

public class Generator {
  
  public static List<String> generate10Names() {
    return generateEnumeratedNames(10);
  }
  
  public static List<String> generateEnumeratedNames(int numOfNames) {
    return IntStream.range(0, numOfNames)
        .mapToObj(i -> "John-" + i)
        .collect(Collectors.toList());
  }
  
  public static List<Integer> generateRandomInts(int numberOfInts) {
    Random random = new Random();
    return IntStream.range(0, numberOfInts)
        .map(i -> random.nextInt(100))
        .boxed()
        .collect(Collectors.toList());
  }
}
