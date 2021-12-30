from typing import Callable, Any


def get_input(day_num: int, parser: Callable[[str], Any] = str, sep: str = '\n') -> list:
    entries = open(f'./input/day{day_num}input.txt').read().rstrip().split(sep)
    return [parser(entry) for entry in entries]


