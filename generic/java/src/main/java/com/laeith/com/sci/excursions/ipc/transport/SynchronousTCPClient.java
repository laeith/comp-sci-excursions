package com.laeith.com.sci.excursions.ipc.transport;

import com.google.protobuf.Message;
import com.laeith.com.sci.excursions.utils.ByteUtils;

import java.io.IOException;
import java.io.InputStream;
import java.net.Socket;

public class SynchronousTCPClient implements Transport {
  
  private final Socket socket;
  // TODO: try buffered reader instead of output streams?
  
  public SynchronousTCPClient() throws IOException {
    socket = new Socket(SynchronousTCPServer.HOST, SynchronousTCPServer.PORT);
  }
  
  @Override
  public byte[] receive() throws IOException {
    InputStream inputStream = socket.getInputStream();
    int msgLen = ByteUtils.byteArrayToInt(inputStream.readNBytes(4));
    return inputStream.readNBytes(msgLen);
  }
  
  @Override
  public void send(Message msg) throws IOException {
    var outputStream = socket.getOutputStream();
    outputStream.write(ByteUtils.intToByteArray(msg.getSerializedSize()));
    outputStream.write(msg.toByteArray());
  }
}
