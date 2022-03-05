package com.laeith.com.sci.excursions.wire.json;

import com.dslplatform.json.CompiledJson;

import java.util.List;

@CompiledJson
public class DoublesOnly {
  public double double1 = 1.1234567899;
  public double double2 = 2.1234567899;
  public double double3 = 3.1234567899;
  public double double4 = 4.1234567899;
  public double double5 = 5.1234567899;
  public List<Double> doubles = List.of(1.132314, 2.111111, 3.314155, 4.1231488, 5.12395832);
}
