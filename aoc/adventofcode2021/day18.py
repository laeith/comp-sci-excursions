import ast

from utils import get_input, infinity


# This is where I gave up type hinting completely and started cheering Python dynamic nature
def add_to(snailfish_num, integer, add_to_left):
    if isinstance(snailfish_num, int):
        return snailfish_num + integer

    if add_to_left:
        return [add_to(snailfish_num[0], integer, True), snailfish_num[1]]
    else:
        return [snailfish_num[0], add_to(snailfish_num[1], integer, False)]


def explode(snailfish_num: list, depth_counter: int = 0):
    if isinstance(snailfish_num, int):
        return False, 0, snailfish_num, 0

    if depth_counter == 4:
        return True, snailfish_num[0], 0, snailfish_num[1]

    # Reduce 'leftmost'
    was_reduced, left, last, right = explode(snailfish_num[0], depth_counter + 1)
    if was_reduced:
        return True, left, [last, add_to(snailfish_num[1], right, True)], 0

    # 'leftmost' failed, try one from right
    was_reduced, left, last, right = explode(snailfish_num[1], depth_counter + 1)
    if was_reduced:
        return True, 0, [add_to(snailfish_num[0], left, False), last], right

    return False, 0, snailfish_num, 0


def split(input):
    if isinstance(input, int):
        if input >= 10:
            quotient, remainder = divmod(input, 2)
            return True, [input // 2, quotient + int(bool(remainder))]
        else:
            return False, input

    was_split, return_value = split(input[0])
    if was_split:
        return True, [return_value, input[1]]

    was_split, return_value = split(input[1])
    if was_split:
        return True, [input[0], return_value]

    return was_split, input


def reduce(result):
    was_reduced, was_split = True, False
    while was_reduced or was_split:
        was_reduced, _, result, _ = explode(result)
        if not was_reduced:
            was_split, result = split(result)
    return result


def calculate_magnitude(input):
    return input if isinstance(input, int) else 3 * calculate_magnitude(input[0]) + 2 * calculate_magnitude(input[1])


def part1():
    data = get_input(18, str_to_list_object)
    result = data[0]

    for i in range(1, len(data)):
        result = reduce([result, data[i]])

    return calculate_magnitude(result)


def part2():
    data = get_input(18, str_to_list_object)

    max_magnitude = -infinity

    # Hmm... O(N^2)
    for i in data:
        for k in data:
            if k != i:
                max_magnitude = max(max_magnitude, calculate_magnitude(reduce([i, k])))

    return max_magnitude


# TODO: Marcin: Write it by hand
def str_to_list_object(line: str) -> list:
    return ast.literal_eval(line)
