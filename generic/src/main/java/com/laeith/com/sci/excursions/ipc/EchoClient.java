package com.laeith.com.sci.excursions.ipc;

import com.laeith.com.sci.excursions.ipc.transport.TCPClient;
import com.laeith.com.sci.excursions.ipc.transport.Transport;
import com.laeith.com.sci.excursions.utils.StaticData;
import com.laeith.playground.protobuf.messages.Core;

import java.io.IOException;

/**
 * This is the 'client' side for all IPC simulations. Can be thought of as a JVM#1 as provided in
 */
public class EchoClient {
  
  private static int idCounter = 1;
  
  public static void main(String[] args) throws InterruptedException, IOException {
    String transportType = System.getProperty("transportType");
    
    System.out.println("Starting Client for: " + transportType);
    
    Transport transport = getTransportClient(transportType);
    
    while (true) {
      Thread.sleep(5000);
      
      Core.Ping pingMsg = Core.Ping.newBuilder()
          .setId(idCounter++)
          .setMessage("Some Test Message")
          .setIsImportant(true)
          .addAllNames(StaticData.NAMES)
          .addAllInts(StaticData.INTS)
          .addAllDoubles(StaticData.DOUBLES)
          .build();
      
      System.out.println("Sending: " + pingMsg);
      
      transport.send(pingMsg);
    }
    
  }
  
  private static Transport getTransportClient(String transportType) throws IOException {
    return switch (transportType) {
      case "TCP" -> new TCPClient();
      case "UDP" -> throw new UnsupportedOperationException("NotImplemented");
      case "File" -> throw new UnsupportedOperationException("NotImplemented");
      case "NamedPipe" -> throw new UnsupportedOperationException("NotImplemented");
      case "mmap" -> throw new UnsupportedOperationException("NotImplemented");
      default -> throw new UnsupportedOperationException("Provided transport type is not supported");
    };
  }
}
