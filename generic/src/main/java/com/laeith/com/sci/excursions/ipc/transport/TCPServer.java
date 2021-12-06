package com.laeith.com.sci.excursions.ipc.transport;

import com.google.protobuf.Message;
import com.laeith.com.sci.excursions.utils.ByteUtils;

import java.io.IOException;
import java.io.InputStream;
import java.net.ServerSocket;
import java.net.Socket;

public class TCPServer implements Transport {
  
  public static final int PORT = 8080;
  public static final String HOST = "localhost";
  
  private final Socket activeSocket;
  
  public TCPServer() throws IOException {
      ServerSocket serverSocket = new ServerSocket(PORT);
      activeSocket = serverSocket.accept();
  }
  
  @Override
  public byte[] receive() throws IOException {
    InputStream inputStream = activeSocket.getInputStream();
    byte[] msgLength = inputStream.readNBytes(4);
    if (msgLength.length != 0) {
      int msgLen = ByteUtils.byteArrayToInt(msgLength);
      return inputStream.readNBytes(msgLen);
    }
    return new byte[]{}; // end of stream
  }
  
  @Override
  public void send(Message msg) throws IOException {
    activeSocket.getOutputStream().write(msg.toByteArray());
  }
}
