package com.laeith.com.sci.excursions.utils;

import java.util.Collections;
import java.util.List;

public class StaticData {
  
  public static final List<String> NAMES = Collections.unmodifiableList(Generator.generateEnumeratedNames(3));
  public static final List<Integer> INTS = List.of(1, 22, 333, 4444, 55555);
  
  public static final List<Double> DOUBLES = List.of(1.132314, 2.111111, 3.314155, 4.1231488, 5.12395832);
  
  public static final double[] DOUBLES_ARRAY = new double[]{1.132314, 2.111111, 3.314155, 4.1231488, 5.12395832};
  
  public static final String REASONABLY_LONG_STRING = "Maybe some reasonably long string, just a few words";
  
}
