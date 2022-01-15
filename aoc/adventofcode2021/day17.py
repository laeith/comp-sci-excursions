from math import sqrt

from utils import Point, get_input

SpeedVector = (int, int)


# 4560
def part1():
    data = get_input(17, lambda line: line.split(","))
    left, right = data[0]
    y_min, y_max = int(right[right.index("=") + 1: right.index("..")]), int(right[right.index("..") + 2:])

    max_y_starting = abs(y_min) - 1

    return (max_y_starting * (max_y_starting + 1)) // 2


def simulate_step(speed_vector: SpeedVector, position: Point) -> (SpeedVector, Point):
    new_position = (position[0] + speed_vector[0], position[1] + speed_vector[1])

    y_speed = speed_vector[1] - 1
    x_speed = speed_vector[0]
    if x_speed < 0:
        x_speed += 1
    if x_speed > 0:
        x_speed -= 1

    return (x_speed, y_speed), new_position


def can_hit(speed_vector: Point, x_min, x_max, y_min, y_max):
    position = (0, 0)

    while True:
        speed_vector, position = simulate_step(speed_vector, position)
        if x_min <= position[0] <= x_max and y_min <= position[1] <= y_max:
            return True
        elif position[1] < y_min:  # we missed the target
            return False


# 3344
def part2():
    data = get_input(17, lambda line: line.split(","))
    left, right = data[0]
    x_min, x_max = int(left[left.index("=") + 1: left.index("..")]), int(left[left.index("..") + 2:])
    y_min, y_max = int(right[right.index("=") + 1: right.index("..")]), int(right[right.index("..") + 2:])

    max_y_starting = abs(y_min) - 1
    min_x_starting = int(sqrt(abs(2 * x_min)))

    count = 0

    # Brute force all the way!
    for x in range(min_x_starting, x_max + 1):
        for y in range(y_min, max_y_starting + 1):
            count += can_hit((x, y), x_min, x_max, y_min, y_max)

    # Took 1s

    return count
