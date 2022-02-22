package com.laeith.com.sci.excursions.funkyjava;

class A {
  public static final int X = B.Y + 1;
}

class B {
  public static final int Y = A.X + 1;
}

public class StaticInitialization {
  public static void main(String[] args) {
    System.out.println("X = " + A.X + ", Y = " + B.Y);
    assert A.X == 2;
    assert B.Y == 1;
  }
}
