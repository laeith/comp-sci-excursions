package com.laeith.com.sci.excursions.funkyjava;

public class FunkyJava {
  
  public static void main(String[] args) {
    System.out.println("Funky java");
    
    assert encodingIsFunky() == 2;
    
  }
  
  private static int encodingIsFunky() {
    int x = 1;
    // \u000a x=2;
    return x;
  }
  
}
