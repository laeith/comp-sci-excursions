package com.laeith.com.sci.excursions.utils;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;

public class ArrayUtilTest {
  
  @Test
  public void testSwap() throws Exception {
    int[] testValues = new int[]{1, 100, 5, 10, 23, -3};
    ArrayUtil.swap(testValues, 0, 3);
    assertEquals(testValues[0], 10);
    assertEquals(testValues[1], 100);
    
    ArrayUtil.swap(testValues, 1, 5);
    assertEquals(testValues[1], -3);
    assertEquals(testValues[5], 100);
  }
}