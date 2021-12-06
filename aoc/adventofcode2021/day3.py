from utils import get_input


def parse_to_list_of_bits(line): return [int(i) for i in line.strip()]


def part1():
    entries = get_input(3, parse_to_list_of_bits)

    bits_grouped_by_position = list(zip(*entries))
    counters_per_position = [sum(bit) for bit in bits_grouped_by_position]

    # A little unreadable, but we make a check that if a sum of 1s on a given position is higher
    # than the number of entries then "gamma" at that position should be "1" else "0"
    # epsilon works similarly, except it's the inverse.
    # I guess the question is what should happen if these are equals? Well, it passes anyway.
    gamma = int("".join(["1" if i > (len(entries) / 2) else "0" for i in counters_per_position]), 2)
    epsilon = int("".join(["1" if i < (len(entries) / 2) else "0" for i in counters_per_position]), 2)

    return gamma * epsilon


def get_most_common_bit_per_position(entries: list) -> list:
    bits_grouped_by_position = list(zip(*entries))
    counters_per_position = [sum(bit) for bit in bits_grouped_by_position]

    return [1 if i >= (len(entries) / 2) else 0 for i in counters_per_position]


def get_least_common_bit_per_position(entries: list) -> list:
    bits_grouped_by_position = list(zip(*entries))
    counters_per_position = [sum(bit) for bit in bits_grouped_by_position]

    return [1 if i < (len(entries) / 2) else 0 for i in counters_per_position]


def part2():
    entries = get_input(3, parse_to_list_of_bits)

    oxygen_ratings = entries
    for position in range(0, len(entries[0])):
        most_common_bit_per_position = get_most_common_bit_per_position(oxygen_ratings)
        oxygen_ratings = list(filter(lambda entry: entry[position] == most_common_bit_per_position[position],
                                     oxygen_ratings))

        if len(oxygen_ratings) == 1:
            break
        elif len(oxygen_ratings) < 1:
            raise ValueError("This shouldn't happen! A bug in logic or flawed input!")

    oxygen_value = int("".join([str(i) for i in oxygen_ratings[0]]), 2)

    co2_ratings = entries
    for position in range(0, len(co2_ratings[0])):
        least_common_bit_per_position = get_least_common_bit_per_position(co2_ratings)
        co2_ratings = list(filter(lambda entry: entry[position] == least_common_bit_per_position[position],
                                  co2_ratings))

        if len(co2_ratings) == 1:
            break
        elif len(co2_ratings) < 1:
            raise ValueError("This shouldn't happen! A bug in logic or flawed input!")

    co2_value = int("".join([str(i) for i in co2_ratings[0]]), 2)

    return co2_value * oxygen_value
