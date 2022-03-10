import math

# length of diagonal and length of side
EXPECTED_NUM_OF_LENGTHS = 2
# 2 form each point
EXPECTED_NUM_OF_SIDES = 8
# 1 from each point
EXPECTED_NUM_OF_DIAGONALS = 4


# https://leetcode.com/problems/valid-square/
def is_square(p1: list[int], p2: list[int], p3: list[int], p4: list[int]):
    points = [p1, p2, p3, p4]
    lengths = {}

    for point1 in points:
        for point2 in points:
            if point1 != point2:
                d = dist(point1, point2)
                if d in lengths:
                    lengths[d] = lengths[d] + 1
                else:
                    lengths[d] = 1

    vals = lengths.values()

    return len(vals) == EXPECTED_NUM_OF_LENGTHS \
           and EXPECTED_NUM_OF_SIDES in vals \
           and EXPECTED_NUM_OF_DIAGONALS in vals


def dist(p1: list[int], p2: list[int]) -> float:
    x1, y1 = p1
    x2, y2 = p2

    return math.sqrt(abs(x1 - x2) ** 2 + abs(y1 - y2) ** 2)


def main():
    assert is_square([0, 0], [1, 1], [1, 0], [0, 1])
    assert not is_square([0, 0], [1, 1], [1, 0], [0, 12])
    assert is_square([1, 0], [-1, 0], [0, 1], [0, -1])
    assert is_square([3, 5], [3, 1], [1, 3], [5, 3])


if __name__ == "__main__":
    main()
