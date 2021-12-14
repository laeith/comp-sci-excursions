from typing import List

from utils import get_input


def parse_to_2d_array_of_ints(line: str) -> List[int]:
    return [int(digit) for digit in line]


def get_neighbours(x, y):
    return [[x - 1, y], [x + 1, y],
            [x, y - 1], [x, y + 1],
            [x - 1, y - 1], [x + 1, y + 1], [x - 1, y + 1], [x + 1, y - 1]]


def is_on_board(x, y, board):
    return 0 <= x < len(board) and 0 <= y < len(board)


def simulate_step(board: List[List[int]]) -> int:
    """
    :return: number of flashed in a given simulation step
    """
    already_flashed = set()

    def uptick_energy_across_board():
        for x in range(0, len(board)):
            for y in range(0, len(board[0])):
                board[x][y] += 1

    def evaluate(x, y):
        energy = board[x][y]
        if energy > 9 and (x, y) not in already_flashed:
            flash(x, y)

    def flash(x, y):
        board[x][y] = 0
        already_flashed.add((x, y))
        for neighbour in [nb for nb in get_neighbours(x, y)
                          if is_on_board(nb[0], nb[1], board)]:
            nb_x, nb_y = neighbour[0], neighbour[1]
            if (nb_x, nb_y) not in already_flashed:
                board[nb_x][nb_y] += 1
                evaluate(nb_x, nb_y)

    uptick_energy_across_board()

    for x in range(0, len(board)):
        for y in range(0, len(board[0])):
            evaluate(x, y)

    return len(already_flashed)


def part1():
    board = get_input(11, parse_to_2d_array_of_ints)

    total_flashes = 0
    for i in range(100):
        total_flashes += simulate_step(board)

    return total_flashes


def part2():
    board = get_input(11, parse_to_2d_array_of_ints)

    step = 0
    octopus_number = sum([len(row) for row in board])
    flashes = 0

    while flashes != octopus_number:
        step += 1
        flashes = simulate_step(board)

    return step
