from collections import deque

from utils import get_input


def part1():
    input = get_input(1, parser=int)

    num_of_increases = 0
    previous_depth_value = input[0]

    for depth in input[1:]:
        if depth > previous_depth_value:
            num_of_increases += 1

        previous_depth_value = depth

    return num_of_increases


def part2():
    input = get_input(1, parser=int)

    num_of_increases = 0

    window = deque()

    window.append(input[0])
    window.append(input[1])
    window.append(input[2])

    previous_window_sum = sum(window)

    for depth in input[3:]:
        window.popleft()
        window.append(depth)

        curr_window_sum = sum(window)
        if curr_window_sum > previous_window_sum:
            num_of_increases += 1

        previous_window_sum = curr_window_sum

    return num_of_increases
