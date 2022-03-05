package com.laeith.com.sci.excursions.utils;

import java.io.IOException;
import java.nio.file.Files;
import java.util.List;

public class Utils {
  
  private static List<String> englishWords = null;
  
  public synchronized static List<String> getEnglishWords() {
    if (englishWords == null) {
      try {
        return Files.readAllLines(FileUtils.getResourcePath("words.txt"));
      } catch (IOException e) {
        throw new RuntimeException("Failed to read words.txt from resources");
      }
    } else {
      return englishWords;
    }
  }
  
  public synchronized static List<List<String>> getEnglishSynonyms() {
    throw new RuntimeException("Not Implemented");
  }
  
  public static int sum(List<Integer> intList) {
    return intList.stream().mapToInt(Integer::intValue).sum();
  }
  
  public static void printIntArray(int[] array) {
    System.out.print("[");
    for (int i = 0; i < array.length; i++) {
      System.out.print(array[i]);
      if (i != array.length - 1) {
        System.out.print(" ");
      }
    }
    System.out.print("]");
    System.out.println();
  }
  
  
}
