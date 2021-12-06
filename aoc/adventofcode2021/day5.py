import functools
from typing import Set, Tuple, List

from utils import get_input


def parse_to_list_of_points(line: str) -> List[List[List[int]]]:
    """
    :return: A list of point pairs e.g. [[['1', 2'], ['1', '7']], [['9', 2'], ['3', '2']]]
    """
    return list(map(lambda entry: entry.strip().split(','), line.split("->")))


def part1() -> int:
    data = get_input(5, parse_to_list_of_points)

    points_vented_at_least_twice = set()
    vented_points = set()
    accumulate = functools.partial(accumulate_points, vented_points, points_vented_at_least_twice)

    for line in data:
        x1, y1 = list(map(int, line[0]))
        x2, y2 = list(map(int, line[1]))

        if x1 == x2:  # is vertical?
            for i in range(min(y1, y2), max(y1, y2) + 1):
                accumulate((x1, i))
        elif y1 == y2:  # is horizontal?
            for i in range(min(x1, x2), max(x1, x2) + 1):
                accumulate((i, y1))
        else:  # is diagonal?
            pass

    return len(points_vented_at_least_twice)


def part2() -> int:
    data = get_input(5, parse_to_list_of_points)

    points_vented_at_least_twice = set()
    vented_points = set()
    accumulate = functools.partial(accumulate_points, vented_points, points_vented_at_least_twice)

    for line in data:
        x1, y1 = list(map(int, line[0]))
        x2, y2 = list(map(int, line[1]))

        if x1 == x2:  # is vertical?
            for i in range(min(y1, y2), max(y1, y2) + 1):
                accumulate((x1, i))
        elif y1 == y2:  # is horizontal?
            for i in range(min(x1, x2), max(x1, x2) + 1):
                accumulate((i, y1))
        else:  # is diagonal?
            dx = x2 - x1
            dy = y2 - y1

            accumulate((x1, y1))
            accumulate((x2, y2))

            assert abs(dx) == abs(dy)  # else it's not diagonal with 45 degrees

            for i in range(1, abs(dx)):
                x = x1 - i if dx <= 0 else x1 + i
                y = y1 - i if dy <= 0 else y1 + i
                accumulate((x, y))

    return len(points_vented_at_least_twice)


def accumulate_points(vented_points: Set[Tuple[int, int]],
                      points_vented_at_least_twice: Set[Tuple[int, int]],
                      point: Tuple[int, int]):
    if point in vented_points:
        points_vented_at_least_twice.add(point)
    vented_points.add(point)
