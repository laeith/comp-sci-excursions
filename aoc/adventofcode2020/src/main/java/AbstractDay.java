import java.io.IOException;
import java.net.URISyntaxException;
import java.net.URL;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;

abstract class AbstractDay {
  
  protected static List<String> pullInput(String inputName) throws URISyntaxException, IOException {
    URL resource = Day1.class.getResource(inputName);
    assert resource != null;
    
    return Files.readAllLines(Path.of(resource.toURI()));
  }
  
}
