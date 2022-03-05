package com.laeith.com.sci.excursions.wire.json;

import com.dslplatform.json.CompiledJson;

import java.util.List;

@CompiledJson
public class PingPongJava {
  public long id;
  public int version;
  public String message;
  public boolean isImportant;
  public List<String> names;
  public List<Integer> ints;
  public List<Double> doubles;
  
  @Override
  public String toString() {
    return "PingPongJava{" +
        "id=" + id +
        ", version=" + version +
        ", message='" + message + '\'' +
        ", isImportant=" + isImportant +
        ", names=" + names +
        ", ints=" + ints +
        ", doubles=" + doubles +
        '}';
  }
}
