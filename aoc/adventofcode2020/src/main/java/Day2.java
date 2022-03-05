import java.io.IOException;
import java.net.URISyntaxException;
import java.util.List;

/**
 * What's the complexity here?
 * Well, the algorithm for isPasswordValid is O(N) so not bad, could be slightly improved by:
 * - Doing an additional check on each matching char if we don't exceed max
 * - Doing an additional check on remaining length and current size if there is enough remaining chars
 * to have a chance to meet the minimum limit
 * But! In practice, this 'optimizations' might actually slow us down! It would be highly dependent on
 * the type of data we get.
 */
public class Day2 extends AbstractDay {
  
  public static void main(String[] args) throws URISyntaxException, IOException {
    final List<String> input = pullInput("Day2Input.txt");
    
    processPart1(input);
    processPart2(input);
  }
  
  private static void processPart1(List<String> input) {
    int validPasswordsCount = 0;
    
    for (String line : input) {
      final String[] lineSplit = line.split(":");
      final String[] policySplit = lineSplit[0].split(" ");
      final String[] rangeSplit = policySplit[0].split("-");
      
      final int minChars = Integer.parseInt(rangeSplit[0]);
      final int maxChars = Integer.parseInt(rangeSplit[1]);
      final char character = policySplit[1].charAt(0);
      
      final String password = lineSplit[1];
      
      if (isPasswordValidPolicy1(password, character, minChars, maxChars)) {
        validPasswordsCount++;
      }
      
    }
    
    System.out.println("Day 2 P1 Answer:");
    System.out.println(validPasswordsCount);
  }
  
  private static boolean isPasswordValidPolicy1(String password, char character, int min, int max) {
    int limitedCharCount = 0;
    for (char c : password.toCharArray()) {
      if (c == character) {
        limitedCharCount++;
      }
    }
    
    return limitedCharCount >= min && limitedCharCount <= max;
  }
  
  private static void processPart2(List<String> input) {
    int validPasswordsCount = 0;
    
    for (String line : input) {
      final String[] lineSplit = line.split(":");
      final String[] policySplit = lineSplit[0].split(" ");
      final String[] positionSplit = policySplit[0].split("-");
      
      final int positionOne = Integer.parseInt(positionSplit[0]);
      final int positionTwo = Integer.parseInt(positionSplit[1]);
      final char character = policySplit[1].charAt(0);
      
      final String password = lineSplit[1].strip();
      
      if (isPasswordValidPolicy2(password, character, positionOne, positionTwo)) {
        validPasswordsCount++;
      }
      
    }
    
    System.out.println("Day 2 P2 Answer:");
    System.out.println(validPasswordsCount);
  }
  
  private static boolean isPasswordValidPolicy2(String password, char character, int positionOne, int positionTwo) {
    final char[] passwordChars = password.toCharArray();
    return passwordChars[positionOne - 1] == character ^ passwordChars[positionTwo - 1] == character;
  }
  
  
}
