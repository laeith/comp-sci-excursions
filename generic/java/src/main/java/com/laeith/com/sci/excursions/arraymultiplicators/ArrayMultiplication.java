package com.laeith.com.sci.excursions.arraymultiplicators;

import java.util.Random;

public abstract class ArrayMultiplication implements Runnable {
  
  protected int arraySize;
  protected int[][] arr1;
  protected int[][] arr2;
  
  public ArrayMultiplication(int arraySize) {
    this.arraySize = arraySize;
    arr1 = generateArrayWithRandomValues(arraySize);
    arr2 = generateArrayWithRandomValues(arraySize);
  }
  
  private int[][] generateArrayWithRandomValues(int arraySize) {
    int[][] res = new int[arraySize][arraySize];
    Random rand = new Random();
    for (int i = 0; i < arraySize; i++) {
      for (int j = 0; j < arraySize; j++) {
        res[i][j] = rand.nextInt(3000);
      }
    }
    return res;
  }
  
}

