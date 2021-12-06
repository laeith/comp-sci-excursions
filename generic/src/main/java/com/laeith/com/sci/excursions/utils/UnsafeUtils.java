package com.laeith.com.sci.excursions.utils;

import sun.misc.Unsafe;

import java.lang.reflect.Field;
import java.security.AccessController;
import java.security.PrivilegedActionException;
import java.security.PrivilegedExceptionAction;

public class UnsafeUtils {
  public static final Unsafe UNSAFE;
  public static final int ARRAY_BYTE_BASE_OFFSET;
  
  static {
    Unsafe unsafe = null;
    final PrivilegedExceptionAction<Unsafe> action =
        () -> {
          final Field f = Unsafe.class.getDeclaredField("theUnsafe");
          f.setAccessible(true);
  
          return (Unsafe) f.get(null);
        };
    
    try {
      unsafe = AccessController.doPrivileged(action);
    } catch (PrivilegedActionException e) {
      e.printStackTrace();
    }
    
    UNSAFE = unsafe;
    ARRAY_BYTE_BASE_OFFSET = Unsafe.ARRAY_BYTE_BASE_OFFSET;
  }
}
