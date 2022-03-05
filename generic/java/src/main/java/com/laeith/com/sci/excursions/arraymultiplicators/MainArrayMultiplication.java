package com.laeith.com.sci.excursions.arraymultiplicators;

import com.laeith.com.sci.excursions.utils.Measurer;

import java.util.concurrent.TimeUnit;

/**
 * Test is based on "What every programmer should know about memory" by Ulrich Drepper
 * Section 6.2.1 Optimizing Level 1 Data Cache Access.
 * While on my machine the 'correct' implementation takes only ~14% the time needed for 'incorrect' one it is still
 * possible to improve it even further.
 */
public class MainArrayMultiplication {
  
  private static final int ARRAY_SIZE = 1_000;
  private static final int TEST_SIZE = 10;
  
  public static void main(String[] args) {
    IncorrectArrayMultiplication iam = new IncorrectArrayMultiplication(ARRAY_SIZE);
    CorrectArrayMultiplication cam = new CorrectArrayMultiplication(ARRAY_SIZE);
    
    Measurer measurer = new Measurer(TEST_SIZE);
    
    measurer.measureAndPrintPretty(iam, TimeUnit.MILLISECONDS);
    measurer.measureAndPrintPretty(cam, TimeUnit.MILLISECONDS);
  }
}
