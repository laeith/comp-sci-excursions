package com.laeith.com.sci.excursions.utils;

import java.io.IOException;
import java.net.URI;
import java.net.URISyntaxException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.stream.Stream;

public class FileUtils {
  
  public static Stream<String> readResourceFile(String fileName) throws IOException {
    return Files.lines(getResourcePath(fileName));
  }
  
  public static Path getResourcePath(String resourcePath) {
    return Paths.get(getResourceURI(resourcePath));
  }
  
  public static URI getResourceURI(String resourcePath) {
    try {
      ClassLoader classLoader = Thread.currentThread().getContextClassLoader();
      return classLoader.getResource(resourcePath).toURI();
    } catch (URISyntaxException e) {
      throw new RuntimeException("Failed to create URI for provided resource path");
    }
  }
  
}
