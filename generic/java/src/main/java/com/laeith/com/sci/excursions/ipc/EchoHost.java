package com.laeith.com.sci.excursions.ipc;

import com.laeith.com.sci.excursions.ipc.transport.SynchronousTCPServer;
import com.laeith.com.sci.excursions.ipc.transport.Transport;
import com.laeith.com.sci.excursions.utils.StaticData;
import com.laeith.playground.protobuf.messages.Core;

import java.io.IOException;

/**
 * Mirroring host, it expects Ping messages and replies with Pong.
 * <p>
 * This seems to be a pretty bad implementation, it gives me ~4k ping-pong msgs / s
 */
public class EchoHost {
  
  public static void main(String[] args) throws IOException {
    String transportType = System.getProperty("transportType", "TCP");
  
    System.out.println("Starting Echo server with mode:" + transportType);
  
    Transport transport = getEchoTransport(transportType);
  
    System.out.println("Connection established - client connected");
  
    Core.Pong pong = Core.Pong.newBuilder()
        .setId(123)
        .setMessage("Some Test Message")
        .setIsImportant(true)
        .addAllNames(StaticData.NAMES)
        .addAllInts(StaticData.INTS)
        .addAllDoubles(StaticData.DOUBLES)
        .build();
  
    while (true) {
      byte[] data = transport.receive();
      if (data.length != 0) {
        //Core.Ping ping = Core.Ping.parseFrom(data);
      
        transport.send(pong);
      } else {
        System.out.println("Connection closed - test finished");
        return;
      }
    }
  }
  
  private static Transport getEchoTransport(String transportType) throws IOException {
    return switch (transportType) {
      case "TCP" -> new SynchronousTCPServer();
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
