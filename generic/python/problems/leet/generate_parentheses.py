# https://leetcode.com/problems/generate-parentheses/


# 1 <= n <= 8
def generate_parentheses(n: int) -> list[str]:
    def backtrack(combinations, current, opened, closed, max):
        if len(current) == max * 2:
            combinations.append(current)
            return

        if opened < max:
            backtrack(combinations, current + '(', opened + 1, closed, max)
        if closed < opened:
            backtrack(combinations, current + ')', opened, closed + 1, max)

    combinations = []
    backtrack(combinations, "", 0, 0, n)
    return combinations


def main():
    print(generate_parentheses(3))
    print(len(generate_parentheses(8)))

    assert generate_parentheses(3) == ["((()))", "(()())", "(())()", "()(())", "()()()"]
    assert generate_parentheses(1) == ["()"]


if __name__ == "__main__":
    main()
