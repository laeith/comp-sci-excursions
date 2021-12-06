from typing import Callable, Any

import day6


def get_input(day_num: int, parser: Callable[[str], Any] = str, sep: str = '\n') -> list:
    entries = open(f'./input/day{day_num}input.txt').read().rstrip().split(sep)
    return [parser(entry) for entry in entries]


def bitlist_to_int(bitlist: list) -> int:
    out = 0
    for bit in bitlist:
        out = (out << 1) | bit


if __name__ == "__main__":
    print(day6.part1())
    pass
