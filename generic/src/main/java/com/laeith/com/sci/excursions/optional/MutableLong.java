package com.laeith.com.sci.excursions.optional;

public class MutableLong {
  public long value = 0;
  
  public MutableLong set(int i) {
    this.value = i;
    return this;
  }
}
