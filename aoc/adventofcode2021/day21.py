from functools import cache

from utils import get_input, get_ints


def roll_fixed_dice(turn):
    rolled = []
    next_roll = turn * 3 + 1
    for roll in range(next_roll, next_roll + 3):
        rolled.append(roll % 100 or 100)
    return rolled


def calculate_new_pos(curr_pos, move):
    return (curr_pos + move) % 10 or 10


def play(start_position_p1, start_position_p2):
    game_state = {
        1: {"position": start_position_p1, "score": 0},
        2: {"position": start_position_p2, "score": 0}
    }

    turn = 0
    while game_state[1]["score"] < 1000 and game_state[2]["score"] < 1000:
        player = turn % 2 + 1

        move = sum(roll_fixed_dice(turn))

        pos, score = game_state[player]["position"], game_state[player]["score"]
        new_pos = calculate_new_pos(pos, move)

        game_state[player]["position"] = new_pos
        game_state[player]["score"] = score + new_pos

        turn += 1

    rolled_times = turn * 3
    if game_state[1]["score"] >= 1000:
        return game_state[2]["score"] * rolled_times
    else:
        return game_state[1]["score"] * rolled_times


def part1():
    data = get_input(21, get_ints)
    return play(int(data[0][1]), int(data[1][1]))


@cache  # without memoization it will never finish
def play_dirac(p1pos, p1score, p2pos, p2score):
    p1wins = p2wins = 0

    for r1 in range(1, 4):
        for r2 in range(1, 4):
            for r3 in range(1, 4):
                new_position = calculate_new_pos(p1pos, r1 + r2 + r3)
                new_score = p1score + new_position
                if new_score >= 21:
                    p1wins += 1
                else:
                    # Alternate players - see arguments
                    new_p2wins, new_p1wins = play_dirac(p2pos, p2score, new_position, new_score)
                    p1wins += new_p1wins
                    p2wins += new_p2wins

    return p1wins, p2wins


# Unfortunately, my solution for part 1 is almost completely useless in part 2
def part2():
    data = get_input(21, get_ints)

    p1pos = int(data[0][1])
    p2pos = int(data[1][1])
    p1score = p2score = 0

    p1wins, p2wins = play_dirac(p1pos, p1score, p2pos, p2score)
    return max(p1wins, p2wins)
