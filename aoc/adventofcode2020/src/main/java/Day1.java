import java.io.IOException;
import java.net.URISyntaxException;
import java.util.List;

/**
 * Seems similar to a subset sum problem, which is NP, with a caveat that we're
 * looking only for 2 ints.
 * <p>
 * Maybe we can sort it beforehand O(NlogN) and leverage binary search O(logN)?
 * <p>
 * P1: Actually, let's keep it simple, the input contains only 400 numbers. -> N^2
 * P2: Well, N^3 is quite... bad - but again, instantaneous for my PC
 */
public class Day1 extends AbstractDay {
  private static final int SUM = 2020;
  
  public static void main(String[] args) throws URISyntaxException, IOException {
    final List<String> inputs = pullInput("Day1P1Input.txt");
    
    processPart1(inputs);
    processPart2(inputs);
  }
  
  private static int find2NumbersMultiplicationThatSumTo(int twoNumberSum, int[] inputs) {
    for (int i = 0; i < inputs.length; i++) {
      for (int j = i + 1; j < inputs.length; j++) {
        if (inputs[i] + inputs[j] == twoNumberSum) {
          return inputs[i] * inputs[j];
        }
      }
    }
    throw new RuntimeException("Summation not found!");
  }
  
  private static long find3NumbersMultiplicationThatSumTo(int threeNumberSum, int[] inputs) {
    for (int i = 0; i < inputs.length; i++) {
      for (int j = i + 1; j < inputs.length; j++) {
        for (int k = j + 1; k < inputs.length; k++) {
          if (inputs[i] + inputs[j] + inputs[k] == threeNumberSum) {
            return (long) inputs[i] * (long) inputs[j] * (long) inputs[k];
          }
        }
      }
    }
    throw new RuntimeException("Summation not found!");
  }
  
  private static void processPart1(List<String> input) {
    final int[] intNumbers = input.stream().mapToInt(Integer::parseInt).toArray();
    
    System.out.println("Day 1 Part 1 answer:");
    System.out.println(find2NumbersMultiplicationThatSumTo(SUM, intNumbers));
  }
  
  private static void processPart2(List<String> input) {
    final int[] intNumbers = input.stream().mapToInt(Integer::parseInt).toArray();
    
    System.out.println("Day 1 Part 2 answer:");
    System.out.println(find3NumbersMultiplicationThatSumTo(SUM, intNumbers));
  }
}
