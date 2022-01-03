from typing import Callable, Any

infinity = float("inf")


def get_input(day_num: int, parser: Callable[[str], Any] = str, sep: str = '\n') -> list:
    entries = open(f'./input/day{day_num}input.txt').read().rstrip().split(sep)
    return [parser(entry) for entry in entries]


Point = tuple[int, int]  # (x, y) points on a grid

neighbors4 = ((0, 1), (1, 0), (0, -1), (-1, 0))


def create_grid(rows: list[list[any]]) -> dict[Point:any]:
    return {(x, y): val
            for y, row in enumerate(rows)
            for x, val in enumerate(row)}


def grid_width(grid: dict[Point: any]) -> int:
    return max(x for x, y in grid) + 1


def grid_height(grid: dict[Point: any]) -> int:
    return max(y for x, y in grid) + 1


def get_neighbors_4(point: Point, grid: dict):
    x, y = point
    return [(x + dx, y + dy) for (dx, dy) in neighbors4
            if (x + dx, y + dy) in dict]


def grid_to_rows(grid: dict):
    return [[grid[x, y] for x in range(grid_width(grid))]
            for y in range(grid_height(grid))]
