from queue import PriorityQueue

from utils import get_input, create_grid, grid_width, grid_height, grid_to_rows


def get_neighbours(point: (int, int)) -> list[(int, int)]:
    x, y = point
    return [(x - 1, y), (x + 1, y),
            (x, y - 1), (x, y + 1)]


def is_within_bounds(point: (int, int), cave_map: list[list[int]]):
    x, y = point
    return 0 <= x < len(cave_map) and 0 <= y < len(cave_map[0])


def dijskra(cave_map: list[list[int]]) -> int:
    starting_point = (0, 0)
    destination_point = (len(cave_map) - 1, len(cave_map[0]) - 1)

    cost_map = {starting_point: 0}

    visited = set()

    to_visit = PriorityQueue()
    to_visit.put((0, starting_point))

    while not to_visit.empty():
        curr_cost, curr_point = to_visit.get()
        if curr_point in visited: continue  # we might add a point twice to the queue before it's visited

        visited.add(curr_point)
        neighbours = [nb for nb in get_neighbours(curr_point) if is_within_bounds(nb, cave_map) and nb not in visited]

        for neighbour in neighbours:
            neighbour_cost = curr_cost + cave_map[neighbour[0]][neighbour[1]]

            if neighbour in cost_map:
                if cost_map[neighbour] > neighbour_cost:
                    cost_map[neighbour] = neighbour_cost
                    to_visit.put((neighbour_cost, neighbour))
            else:
                cost_map[neighbour] = neighbour_cost
                to_visit.put((neighbour_cost, neighbour))

    return cost_map[destination_point]


# I blindly started with DFS, given that it's relatively quick to implement and hoping it would be enough,
# maybe with some additional optimizations...
# But then I saw the main input and realized that for the optimum I need to traverse almost everything anyway which
# usually is feasible for reasonably sized graphs, or if our goal is to visit all possible nodes,
# but this one is actually pretty huge.
# So Dijskra or A*?
# A* should probably work better given that we have a relatively good heuristic that following a diagonal
# should be close to the optimal path
# Anyway, this is another great example where naive DFS takes ages while a better algorithm (Dijskra) is almost
# instantaneous
# 40
def part1():
    cave_map: list[list[int]] = get_input(15, lambda line: [int(risk_level) for risk_level in line])
    return dijskra(cave_map)


# 2907
# TODO: Marcin: Rework this...
def part2():
    cave_map: list[list[int]] = get_input(15, lambda line: [int(risk_level) for risk_level in line])

    new_cave_grid = create_grid(cave_map)

    width = grid_width(new_cave_grid)
    height = grid_height(new_cave_grid)

    for i in range(1, 5):
        for x in range(width):
            for y in range(height):
                new_cave_grid[(i * width + x, y)] = modified_mod(new_cave_grid[(i - 1) * width + x, y] + 1, 9)

    width = grid_width(new_cave_grid)
    height = grid_height(new_cave_grid)

    for i in range(1, 5):
        for x in range(width):
            for y in range(height):
                new_cave_grid[(x, i * height + y)] = modified_mod(new_cave_grid[x, (i - 1) * height + y] + 1, 9)

    return dijskra(grid_to_rows(new_cave_grid))


def modified_mod(number: int, mod_value: int) -> int:
    """Returns a mod of a given number, except that instead of 0 we get mod value"""
    return (number % mod_value) or mod_value
