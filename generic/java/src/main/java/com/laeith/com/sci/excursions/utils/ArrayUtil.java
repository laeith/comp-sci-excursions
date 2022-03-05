package com.laeith.com.sci.excursions.utils;

import java.util.concurrent.ThreadLocalRandom;

public final class ArrayUtil {
  
  private ArrayUtil() {
    throw new AssertionError();
  }
  
  public static void swap(int[] array, int posOne, int posTwo) {
    int tempValue = array[posOne];
    array[posOne] = array[posTwo];
    array[posTwo] = tempValue;
  }
  
  public static int[] getRandomData(int n) {
    int[] vals = new int[n];
    for (int i = 0; i < n; i++) {
      vals[i] = ThreadLocalRandom.current().nextInt(1, 50);
    }
    return vals;
  }
  
  public static void printIntArray(int[] array) {
    StringBuilder sb = new StringBuilder("[");
    for (int i1 : array) {
      sb.append(i1).append(" ");
    }
    sb.deleteCharAt(sb.length() - 1);
    sb.append("]");
    System.out.println(sb);
  }
}
