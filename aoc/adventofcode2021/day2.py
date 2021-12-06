from utils import get_input


def parse_submarine_commands(entry: str):
    split = entry.split(' ')
    return split[0], int(split[1])


def part1():
    commands = get_input(2, parse_submarine_commands)

    pos = {
        "horizontal": 0,
        "depth": 0
    }

    # Looks like lambdas are not that great in Python, this would be a good use case for pattern matching
    # or getattr() abuse
    available_commands = {
        "forward": (lambda value: pos.__setitem__("horizontal", pos["horizontal"] + value)),
        "up": (lambda value: pos.__setitem__("depth", pos["depth"] - value)),
        "down": (lambda value: pos.__setitem__("depth", pos["depth"] + value)),
    }

    for command in commands:
        available_commands[command[0]](command[1])

    return pos["horizontal"] * pos["depth"]


def part2():
    commands = get_input(2, parse_submarine_commands)

    pos = {
        "horizontal": 0,
        "depth": 0,
        "aim": 0
    }

    def execute_forward(value):
        pos["horizontal"] += value
        pos["depth"] += pos["aim"] * value

    available_commands = {
        "forward": lambda value: execute_forward(value),
        "up": lambda value: pos.__setitem__("aim", pos["aim"] - value),
        "down": lambda value: pos.__setitem__("aim", pos["aim"] + value),
    }

    for command in commands:
        available_commands[command[0]](command[1])

    return pos["horizontal"] * pos["depth"]
