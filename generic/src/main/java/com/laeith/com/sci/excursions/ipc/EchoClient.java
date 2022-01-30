package com.laeith.com.sci.excursions.ipc;

import com.laeith.com.sci.excursions.ipc.transport.SynchronousTCPClient;
import com.laeith.com.sci.excursions.ipc.transport.Transport;
import com.laeith.com.sci.excursions.utils.StaticData;
import com.laeith.playground.protobuf.messages.Core;

import java.io.IOException;

/**
 * This is the 'client' side for all IPC simulations. Can be thought of as a JVM#1 as provided in
 */
public class EchoClient {
  
  private static int idCounter = 1;
  
  private static final int NUM_OF_PING_PONGS = 1_000_000;
  
  public static void main(String[] args) throws InterruptedException, IOException {
    String transportType = System.getProperty("transportType", "TCP");
    
    System.out.println("Starting Echo Client with mode: " + transportType);
    
    Transport transport = getTransportClient(transportType);
    
    long startTime = System.nanoTime();
    
    Core.Ping pingMsg = Core.Ping.newBuilder()
        .setId(124)
        .setMessage("Some Test Message")
        .setIsImportant(true)
        .addAllNames(StaticData.NAMES)
        .addAllInts(StaticData.INTS)
        .addAllDoubles(StaticData.DOUBLES)
        .build();
    
    
    while (idCounter < NUM_OF_PING_PONGS) {
      if (idCounter % 10000 == 0) {
        System.out.println("Processed " + idCounter + " ping pongs");
      }
      
      idCounter++;
      
      transport.send(pingMsg);
      
      byte[] data = transport.receive();
      if (data.length != 0) {
        //Core.Pong pong = Core.Pong.parseFrom(data);
      }
    }
    
    long endTime = System.nanoTime();
    
    double seconds = (endTime - startTime) * Math.pow(10, -9);
    
    System.out.println("Test completed, processed: " + idCounter + " ping pongs in " + seconds + " seconds");
    System.out.println("Average throughput: " + idCounter / seconds + " ping pongs / s");
    
  }
  
  private static Transport getTransportClient(String transportType) throws IOException {
    return switch (transportType) {
      case "TCP" -> new SynchronousTCPClient();
      case "UDP" -> throw new UnsupportedOperationException("NotImplemented");
      case "File" -> throw new UnsupportedOperationException("NotImplemented");
      case "NamedPipe" -> throw new UnsupportedOperationException("NotImplemented");
      case "mmap" -> throw new UnsupportedOperationException("NotImplemented");
      default -> throw new UnsupportedOperationException("Provided transport type is not supported");
    };
  }
}
