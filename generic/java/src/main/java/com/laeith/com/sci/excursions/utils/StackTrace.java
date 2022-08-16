package com.laeith.com.sci.excursions.utils;

import java.util.Arrays;

/**
 * Programmatic way of 'logging' a given code place / thread execution state.
 * This is useful to track back from where we e.g. created a given object, or where we closed a given resource etc.
 * <p>
 * This was inspired by Peter Lawrey work.
 */
public class StackTrace extends Throwable {
  
  public StackTrace(String message) {
    this(message, null);
  }
  
  public StackTrace(String message, Throwable cause) {
    super(message + " on " + Thread.currentThread().getName(), cause);
  }
  
  public static StackTrace forThread(Thread thread) {
    StackTrace st = new StackTrace(thread.toString());
    st.setStackTrace(thread.getStackTrace());
    return st;
  }
  
  @Override
  public int hashCode() {
    return Arrays.hashCode(getStackTrace());
  }
  
  @Override
  public boolean equals(Object obj) {
    if (obj == this) {
      return true;
    }
    
    if (!(obj instanceof StackTrace other)) {
      return false;
    }
    
    return Arrays.equals(other.getStackTrace(), this.getStackTrace());
  }
  
}
