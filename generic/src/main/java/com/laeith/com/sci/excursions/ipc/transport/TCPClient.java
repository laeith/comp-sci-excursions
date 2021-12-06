package com.laeith.com.sci.excursions.ipc.transport;

import com.google.protobuf.Message;
import com.laeith.com.sci.excursions.utils.ByteUtils;

import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.Socket;

public class TCPClient implements Transport {
  
  private final Socket socket;
  // TODO: try buffered reader instead of output streams?
  
  public TCPClient() throws IOException {
    socket = new Socket(TCPServer.HOST, TCPServer.PORT);
  }
  
  @Override
  public byte[] receive() throws IOException {
    InputStream inputStream = socket.getInputStream();
    int msgLen = ByteUtils.byteArrayToInt(inputStream.readNBytes(4));
    return inputStream.readNBytes(msgLen);
  }
  
  @Override
  public void send(Message msg) throws IOException {
    OutputStream outputStream = socket.getOutputStream();
    outputStream.write(ByteUtils.intToByteArray(msg.getSerializedSize()));
    outputStream.write(msg.toByteArray());
  }
}
