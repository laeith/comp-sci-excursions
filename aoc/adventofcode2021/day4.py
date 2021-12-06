import functools
from typing import List

from utils import get_input


# Actually, it seems to be possible to optimize it by quite a lot
# e.g. instead of iterating and checking every single number in row/column we could
# start removing them when 'seen' and declare a winning board when any single row/column is empty
# but then again - even now it executes in a blink of an eye
def part1():
    data = list(filter(lambda line: line != '', get_input(4)))
    nums = list(map(int, data[0].split(',')))

    board_row_entries = [[int(value) for value in entry.strip().split()] for entry in data[1:]]
    num_of_boards = int(len(board_row_entries) / 5)
    boards_by_rows = [board_row_entries[i * 5: i * 5 + 5] for i in range(num_of_boards)]
    boards_by_columns = [list(zip(*board)) for board in boards_by_rows]

    winning_board_id, seen_numbers = find_first_winning_board(boards_by_rows, boards_by_columns, nums)
    winning_number = seen_numbers[-1]

    sum_of_not_seen_numbers = sum_not_seen(boards_by_rows[winning_board_id], seen_numbers)

    return sum_of_not_seen_numbers * winning_number


def sum_not_seen(board: List[List[int]], seen_numbers: List[int]) -> int:
    # This is quite crazy, but I really wanted to try functools.reduce()
    def sum_not_seen_numbers(numbers):
        return functools.reduce(lambda row_sum, num: row_sum + num if num not in seen_numbers else row_sum, numbers, 0)

    return sum(map(sum_not_seen_numbers, board))


def find_first_winning_board(boards_by_rows, boards_by_columns, nums):
    seen_numbers = []
    for number in nums:
        seen_numbers.append(number)

        for board_id in range(len(boards_by_rows)):
            for k in range(5):
                if is_winning_array(boards_by_rows[board_id][k], seen_numbers) \
                        or is_winning_array(boards_by_columns[board_id][k], seen_numbers):
                    return board_id, seen_numbers


def is_winning_array(row: List[int], winning_numbers: List[int]) -> bool:
    for num in row:
        if num not in winning_numbers:
            return False
    return True


# TODO: Marcin: Clean it up?
def part2():
    data = list(filter(lambda line: line != '', get_input(4)))
    nums = list(map(int, data[0].split(',')))

    board_row_entries = [[int(value) for value in entry.strip().split()] for entry in data[1:]]
    num_of_boards = int(len(board_row_entries) / 5)
    boards_by_rows = [board_row_entries[i * 5: i * 5 + 5] for i in range(num_of_boards)]
    boards_by_columns = [list(zip(*board)) for board in boards_by_rows]

    finished_boards = []
    seen_numbers = []

    # Behold the beauty!
    for number in nums:
        seen_numbers.append(number)
        for board_id in range(len(boards_by_rows)):
            for k in range(5):
                if is_winning_array(boards_by_rows[board_id][k], seen_numbers) \
                        or is_winning_array(boards_by_columns[board_id][k], seen_numbers):
                    if board_id not in finished_boards:
                        finished_boards.append(board_id)
                        if len(finished_boards) == len(boards_by_rows):
                            return sum_not_seen(boards_by_rows[finished_boards[-1]], seen_numbers) * number
