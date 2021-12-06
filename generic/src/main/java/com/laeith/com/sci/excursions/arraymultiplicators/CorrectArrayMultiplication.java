package com.laeith.com.sci.excursions.arraymultiplicators;

public class CorrectArrayMultiplication extends ArrayMultiplication {
  
  int[][] transArr = new int[arraySize][arraySize];
  
  public CorrectArrayMultiplication(int arraySize) {
    super(arraySize);
  }
  
  @Override
  public void run() {
    transArr = transposition(arr2); // despite this copy call it's still much more efficient - yet it's nice to keep in mind
    // that this copy might be costly in real environment.
    correctMultiply(arr1, transArr);
  }
  
  /**
   * Transposition is required to make sure that we iterate sequentially through array in memory.
   * Sequential calls on the same row in memory is much more efficient then accessing memory on
   * different rows and different columns.
   */
  private int[][] transposition(int[][] arr2) {
    int[][] temp = new int[arraySize][arraySize];
    for (int i = 0; i < arraySize; i++) {
      for (int j = 0; j < arraySize; j++) {
        temp[i][j] = arr2[j][i];
      }
    }
    return temp;
  }
  
  private int[][] correctMultiply(int[][] arr1, int[][] arr2) {
    int[][] res = new int[arraySize][arraySize];
    for (int i = 0; i < arraySize; i++) {
      for (int j = 0; j < arraySize; j++) {
        for (int k = 0; k < arraySize; k++) {
          res[i][j] += arr1[i][k] * arr2[j][k]; // Compared to Incorrect Array Multiplication
        }
      }
    }
    return new int[arraySize][arraySize];
  }
  
  @Override
  public String toString() {
    return "Correct Array Multiplication";
  }
  
}
