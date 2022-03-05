package com.laeith.com.sci.excursions.ipc.transport;

import com.google.protobuf.Message;

import java.io.IOException;

public interface Transport {
  
  byte[] receive() throws IOException;
  
  void send(Message msg) throws IOException;
  
}
