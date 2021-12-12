import functools
from typing import List

from utils import get_input


def parse_note(line: str) -> (List[str], List[str]):
    patterns, digits = line.split("|")
    patterns = patterns.strip().split(" ")
    digits = digits.strip().split(" ")
    return patterns, digits


def part1():
    output_digits = [digit for data in get_input(8, parse_note) for digit in data[1]]  # flatten list

    unique_lengths = {2, 4, 3, 7}

    number_of_unique_digits = functools.reduce(lambda comb, curr: comb + 1 if len(curr) in unique_lengths else comb,
                                               output_digits, 0)
    # Without functools:
    # number_of_unique_digits = sum([1 if len(digit) in unique_lengths else 0 for digit in output_digits])

    return number_of_unique_digits


# This one can also be done 'in reverse' where we actually discover real mapping between segments and only then,
# given that mapping, do: decode segments in values -> map real segments to numbers
# Though that solution was far longer and 'iterative'
def part2():
    data = get_input(8, parse_note)

    result = 0

    for entry in data:
        num_decoded = {num: set('abcdefg') for num in range(10)}

        patterns, values = entry
        patterns = [set([char for char in pattern]) for pattern in
                    sorted(patterns, key=len)]  # this will guarantee to get 1, 4, 7 nums during first 3 matches

        # This is pattern matching for brevity, but it actually relies on patterns being sorted from the lowest length
        # so that we get 4 & 7 decoded before we get to 'complex' patterns
        for pattern in patterns:
            match (len(pattern), len(pattern - num_decoded[4]), len(pattern - num_decoded[7])):
                case (6, 3, 3): num_decoded[0] = pattern
                case (2, _, _): num_decoded[1] = pattern  # unique pattern length
                case (5, 3, 3): num_decoded[2] = pattern
                case (5, _, 2): num_decoded[3] = pattern
                case (4, _, _): num_decoded[4] = pattern  # unique pattern length
                case (5, 2, 3): num_decoded[5] = pattern
                case (6, 3, 4): num_decoded[6] = pattern
                case (3, _, _): num_decoded[7] = pattern  # unique pattern length
                case (7, _, _): num_decoded[8] = pattern  # unique pattern length
                case (6, 2, _): num_decoded[9] = pattern
                case _: print(f"Should not happen, found unknown pattern: {pattern}")

        decoded_number = "".join([str(num) for value in values
                                  for num, decoded_pattern in num_decoded.items()
                                  if set(value) == decoded_pattern])

        # Non list-comprehension version:
        # decoded_number = ""
        # for value in values:
        #     for num, decoded in num_decoded.items():
        #         if set(value) == decoded:
        #             decoded_number += str(num)

        result += int(decoded_number)

    return result
