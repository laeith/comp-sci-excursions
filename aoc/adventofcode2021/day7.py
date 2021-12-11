import functools

from utils import get_input


# I could use statistics module from Python for mean/median calculation
def part1():
    sorted_positions = sorted(get_input(7, int, sep=","))

    n = len(sorted_positions)

    # Median position
    if len(sorted_positions) % 2 == 0:
        opt_position = sorted_positions[n // 2]
    else:
        mid = int(n // 2)
        opt_position = (sorted_positions[mid] + sorted_positions[mid + 1]) // 2

    return sum([abs(i - opt_position) for i in sorted_positions])


def part2():
    data = get_input(7, int, sep=",")

    # Mean position
    opt_position = sum(data) // len(data)

    # Sum for arithmetic sequence
    def fuel_to_position(start_pos, end_pos):
        n = abs(end_pos - start_pos)
        return (n * (1 + n)) // 2

    required_fuel = functools.reduce(lambda prev, curr: prev + fuel_to_position(curr, opt_position), data, 0)
    # Without functools:
    # required_fuel = sum([fuel_to_position(curr, opt_position) for curr in data])

    return required_fuel
