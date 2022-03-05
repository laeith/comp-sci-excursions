package com.laeith.com.sci.excursions.problems.spoj;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.Arrays;

public class AGGRCOW {
  
  public static void main(String[] args) throws Exception {
    BufferedReader stdin = new BufferedReader(new InputStreamReader(System.in));
    int numberOfTestCases = Integer.parseInt(stdin.readLine());
    
    String input;
    while ((input = stdin.readLine()) != null && input.length() != 0) {
      String[] split = input.split(" ");
      int stalls = Integer.parseInt(split[0]);
      int cows = Integer.parseInt(split[1]);
  
      int[] placements = new int[stalls];
  
      for (int z = 0; z < stalls; z++) {
        placements[z] = Integer.parseInt(stdin.readLine());
      }

//      Sort required for binary search
      Arrays.sort(placements);
  
      System.out.println(findMinimumDistance(placements, cows));
    }
  }
  
  public static boolean isThisDistanceAcceptable(int distance, int[] stallPlacements, int cows) {
    int maxCows = 2; // we start with two cows at two stable ends
    int prevCowIndex = 0;
    int lastIndex = stallPlacements.length - 1;
    
    for (int i = 0; i < stallPlacements.length; i++) {
      if ((stallPlacements[lastIndex] - stallPlacements[i]) < distance || maxCows >= cows) {
        break;
      }
      if ((stallPlacements[i] - stallPlacements[prevCowIndex]) >= distance) {
        maxCows++;
        prevCowIndex = i;
      }
    }
    
    return maxCows >= cows;
  }
  
  public static int findMinimumDistance(int[] placements, int cows) {
    int left = 0;
    int right = placements[placements.length - 1];
    
    if (cows == 2) {
      return right - left;
    }
    
    while (left < right) {
      int midDist = (right + left) / 2;
      
      if (isThisDistanceAcceptable(midDist, placements, cows)) {
        left = midDist + 1;
      } else {
        right = midDist;
      }
    }
    
    return left - 1;
  }
  
}
