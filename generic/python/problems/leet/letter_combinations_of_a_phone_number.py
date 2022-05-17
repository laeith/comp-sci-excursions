# https://leetcode.com/problems/letter-combinations-of-a-phone-number/
def main():
    assert letter_combinations("23") == ["ad", "ae", "af", "bd", "be", "bf", "cd", "ce", "cf"]
    assert letter_combinations("1") == []
    assert letter_combinations("2") == ["a", "b", "c"]
    assert letter_combinations("") == []


mapping = {
    "1": [],
    "2": ["a", "b", "c"],
    "3": ["d", "e", "f"],
    "4": ["g", "h", "i"],
    "5": ["j", "k", "l"],
    "6": ["m", "n", "o"],
    "7": ["p", "q", "r", "s"],
    "8": ["t", "u", "v"],
    "9": ["w", "x", "y", "z"],
    "0": [" "],
}


def letter_combinations(digits: str) -> list[str]:
    possible_combinations = []

    # Well, turns out that the input can contain only 2 <= digit <= 9 digits so this check is redundant
    digits = list(filter(lambda digit: digit != "1", digits))  # 1 doesn't matter
    num_of_chars = len(digits)
    if num_of_chars == 0:
        return []

    def take_a_pick(combinations, curr_combination, remaining_digits, max_chars):
        if len(curr_combination) == max_chars:
            combinations.append(curr_combination)
            return

        for possible_choice in mapping[remaining_digits[0]]:
            take_a_pick(combinations, curr_combination + possible_choice, remaining_digits[1:], max_chars)

    take_a_pick(possible_combinations, "", digits, num_of_chars)
    return possible_combinations


if __name__ == "__main__":
    main()
