import functools

from utils import get_input


def parse_to_2d_array(line: str):
    return [int(char) for char in line]


def part1():
    height_map = get_input(9, parse_to_2d_array)

    risk_levels = []

    for col_id in range(len(height_map[0])):
        for row_id in range(len(height_map)):
            is_lowest = True
            value = height_map[row_id][col_id]

            # check if all viable neighbours are higher
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1,)]:
                if is_lowest and (0 <= row_id + dx < len(height_map) and 0 <= col_id + dy < len(height_map[0])):
                    is_lowest = height_map[row_id + dx][col_id + dy] > value

            if is_lowest: risk_levels.append(value + 1)

    return sum(risk_levels)


def part2():
    height_map = get_input(9, parse_to_2d_array)
    seen_points = set()

    def find_basin_size(row_id: int, col_id: int):
        if (
                not (0 <= row_id < len(height_map))  # out of map
                or not (0 <= col_id < len(height_map[0]))  # out of map
                or height_map[row_id][col_id] == 9
                or (row_id, col_id) in seen_points
        ):
            return 0
        else:
            seen_points.add((row_id, col_id))
            return 1 + find_basin_size(row_id - 1, col_id) \
                   + find_basin_size(row_id + 1, col_id) \
                   + find_basin_size(row_id, col_id - 1) \
                   + find_basin_size(row_id, col_id + 1)

    basin_sizes = []

    for col_id in range(len(height_map[0])):
        for row_id in range(len(height_map)):
            basin_sizes.append(find_basin_size(row_id, col_id))

    top_3_biggest_basin_sizes = sorted(basin_sizes, reverse=True)[:3]

    return functools.reduce(lambda comb, curr: comb * curr, top_3_biggest_basin_sizes)
