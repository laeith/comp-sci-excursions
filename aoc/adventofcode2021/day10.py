import functools
from collections import deque

from utils import get_input

opening, closing = '([{<', ')]}>'
open_to_close = dict(zip(opening, closing))


def part1():
    data = get_input(10)

    scoring_map = dict(zip(closing, (3, 57, 1197, 25137)))
    corrupted_chars = []

    for line in data:
        stack = deque()
        for char in line:
            if char in open_to_close:
                stack.append(char)
            elif len(stack) > 0 and open_to_close[stack[-1]] == char:
                stack.pop()
            else:
                corrupted_chars.append(char)
                break

    scores = list(map(lambda char: scoring_map[char], corrupted_chars))

    return sum(scores)


def part2():
    data = get_input(10)

    scoring_map = dict(zip(closing, range(1, 5)))
    scores = []

    for line in data:
        stack = deque()
        corrupted = False

        for char in line:
            if char in open_to_close:
                stack.append(char)
            elif len(stack) > 0 and open_to_close[stack[-1]] == char:
                stack.pop()
            else:
                corrupted = True
                break

        if not corrupted:
            completion_scores = list(map(lambda char: scoring_map[open_to_close[char]], reversed(stack)))
            scores.append(functools.reduce(lambda comb, curr: 5 * comb + curr, completion_scores))

    return sorted(scores)[len(scores) // 2]
