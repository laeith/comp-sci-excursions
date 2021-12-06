package com.laeith.com.sci.excursions.ipc;

import com.laeith.com.sci.excursions.ipc.transport.TCPServer;
import com.laeith.com.sci.excursions.ipc.transport.Transport;
import com.laeith.playground.protobuf.messages.Core;

import java.io.IOException;

/**
 * Mirroring host, it expects Ping messages and replies with Pong.
 */
public class EchoHost {
  
  public static void main(String[] args) throws IOException {
    String transportType = System.getProperty("transportType");
    
    System.out.println("Starting Echo server with " + transportType);
    
    Transport transport = getEchoTransport(transportType);
    
    System.out.println("Connection established");
    
    while (true) {
      byte[] data = transport.receive();
      if (data.length != 0) {
        Core.Ping ping = Core.Ping.parseFrom(data);
        System.out.println("Received: " + ping);
      } else {
        System.out.println("Connection closed");
        return;
      }
    }
  }
  
  private static Transport getEchoTransport(String transportType) throws IOException {
    return switch (transportType) {
      case "TCP" -> new TCPServer();
      case "UDP" -> throw new UnsupportedOperationException("NotImplemented");
      case "File" -> throw new UnsupportedOperationException("NotImplemented");
      case "NamedPipe" -> throw new UnsupportedOperationException("NotImplemented");
      case "mmap" -> throw new UnsupportedOperationException("NotImplemented");
      case "REST" -> throw new UnsupportedOperationException("NotImplemented");
      case "ChronicleQueue" -> throw new UnsupportedOperationException("NotImplemented");
      default -> throw new UnsupportedOperationException("Provided transport type is not supported");
    };
  }
  
}
