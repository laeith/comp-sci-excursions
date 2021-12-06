package com.laeith.com.sci.excursions;

import org.openjdk.jol.info.ClassLayout;
import org.openjdk.jol.info.GraphLayout;
import org.openjdk.jol.vm.VM;

// To run needs to supply -Djdk.attach.allowAttachSelf
public class JOLMain {
  
  public static void main(String[] args) {
    System.out.println("##### Java Object Layout playground #####");
  
    System.out.println(VM.current().details());
    System.out.println(ClassLayout.parseClass(Object.class).toPrintable());
  
    System.out.println("Test Obj:");
  
    Object testObj = new Object();
    System.out.println(GraphLayout.parseInstance(testObj).toFootprint());
  }
}
