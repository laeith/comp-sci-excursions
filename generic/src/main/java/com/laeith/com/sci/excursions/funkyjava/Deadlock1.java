package com.laeith.com.sci.excursions.funkyjava;


public class Deadlock1 {
  public static void main(String[] args) throws InterruptedException {
    Deadlock1 deadlock1 = new Deadlock1();
    new Thread(() -> deadlock1.method("1")).start();
    new Thread(() -> deadlock1.method("2")).start();
  }
  
  void method(String label) {
    Boolean x = true;
    // It will work with this:
    //Boolean x = new Boolean(true);
    synchronized (x) {
      while (true) {
        System.out.println("Running " + label);
        try {
          Thread.sleep(1000);
        } catch (InterruptedException e) {
          e.printStackTrace();
        }
      }
    }
  }
}
