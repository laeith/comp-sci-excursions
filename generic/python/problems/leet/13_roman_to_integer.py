# https://leetcode.com/problems/roman-to-integer/

roman_singles = {
    "I": 1,
    "V": 5,
    "X": 10,
    "L": 50,
    "C": 100,
    "D": 500,
    "M": 1000,
}

roman_doubles = {
    "IV": 4,
    "IX": 9,
    "XL": 40,
    "XC": 90,
    "CD": 400,
    "CM": 900,
}

def roman_to_int(s: str) -> int:
    result = 0

    should_skip_next = False
    for i, char in enumerate(s):
        if should_skip_next:
            should_skip_next = False
            continue

        if len(s) > i + 1:
            potential_double = char + s[i+1]
            if potential_double in roman_doubles:
                result += roman_doubles[potential_double]
                should_skip_next = True
                continue

        result += roman_singles[char]

    return result


def main():
    assert roman_to_int("V") == 5
    assert roman_to_int("IV") == 4
    assert roman_to_int("XIV") == 14
    assert roman_to_int("CMLIII") == 953


if __name__ == "__main__":
    main()

