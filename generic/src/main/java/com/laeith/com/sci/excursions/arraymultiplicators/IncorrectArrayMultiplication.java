package com.laeith.com.sci.excursions.arraymultiplicators;

public class IncorrectArrayMultiplication extends ArrayMultiplication {
  
  public IncorrectArrayMultiplication(int arraySize) {
    super(arraySize);
  }
  
  @Override
  public void run() {
    incorrectMultiply(arr1, arr2);
  }
  
  private int[][] incorrectMultiply(int[][] arr1, int[][] arr2) {
    int[][] res = new int[arraySize][arraySize];
    for (int i = 0; i < arraySize; i++) {
      for (int j = 0; j < arraySize; j++) {
        for (int k = 0; k < arraySize; k++) {
          res[i][j] += arr1[i][k] * arr2[k][j];
        }
      }
    }
    return new int[arraySize][arraySize];
  }
  
  @Override
  public String toString() {
    return "Incorrect Array Multiplication";
  }
}
