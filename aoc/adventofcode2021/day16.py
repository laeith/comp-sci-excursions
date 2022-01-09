from collections import deque
from functools import reduce
from operator import add, mul, lt, gt, eq

from utils import get_input

# When I got to part2 It became clear that my approach is sub-optimal for this particular task, not only it's
# prone to stack-overflows but also the complexity is quite high. Now I think that a better solution would be to
# simply treat it as a stream of data and calculate everything 'in-place', returning the final version sum and value
# but well, it works as is, so maybe next time.

# These are only used for descriptions, technically redundant
TYPE_OPERATOR_MAPPING = {
    0: "sum",
    1: "product",
    2: "minimum",
    3: "maximum",
    4: "literal",
    5: "greater than",
    6: "less than",
    7: "equal to",
}

funcs = [add, mul, min, max, int, gt, lt, eq]


def decode_literal(curr_cursor: int, binary_input: str, literal: str = "") -> (int, str):
    continuation_bit = binary_input[curr_cursor]
    curr_cursor += 1

    match continuation_bit:
        case "0":
            literal_number = str(int(literal + binary_input[curr_cursor:curr_cursor + 4], 2))
            curr_cursor += 4
            return curr_cursor, literal_number
        case "1":
            literal += binary_input[curr_cursor:curr_cursor + 4]
            curr_cursor += 4
            return decode_literal(curr_cursor, binary_input, literal)
        case _:
            raise RuntimeError(f"Unexpected character in binary representation: {continuation_bit}")


def decode_packet(curr_cursor: int, binary_input: str, decoded_output: deque[(int, int, str, list[int])] = deque()) -> (
        int, deque[(int, int, str, list[int])]):
    version = int(binary_input[curr_cursor: curr_cursor + 3], 2)
    curr_cursor += 3
    packet_type = int(binary_input[curr_cursor: curr_cursor + 3], 2)
    curr_cursor += 3

    match packet_type:
        case 4:
            curr_cursor, packet_output = decode_literal(curr_cursor, binary_input)
            decoded_output.append((version, packet_type, packet_output, 1))
            return curr_cursor, decoded_output
        case _:
            sub_packets_length = binary_input[curr_cursor]
            curr_cursor += 1

            sub_packets_num_container = [0]  # uh... poor man's pointer
            decoded_output.append((version, packet_type, TYPE_OPERATOR_MAPPING[packet_type], sub_packets_num_container))

            match sub_packets_length:
                case "0":
                    packets_length = int(binary_input[curr_cursor: curr_cursor + 15], 2)
                    curr_cursor += 15
                    end_cursor = curr_cursor + packets_length

                    num_of_packets = 0
                    while curr_cursor < end_cursor:
                        num_of_packets += 1
                        curr_cursor, decoded_output = decode_packet(curr_cursor, binary_input, decoded_output)
                    sub_packets_num_container[0] = num_of_packets

                    return curr_cursor, decoded_output
                case "1":
                    num_of_packets = int(binary_input[curr_cursor: curr_cursor + 11], 2)
                    curr_cursor += 11
                    for i in range(num_of_packets):
                        curr_cursor, decoded_output = decode_packet(curr_cursor, binary_input, decoded_output)
                    sub_packets_num_container[0] = num_of_packets
                    return curr_cursor, decoded_output

                case _:
                    raise RuntimeError(f"Unexpected character in binary representation: {sub_packets_length}")


def part1():
    hex_input = get_input(16)[0]
    binary_input = ("".join(list(map(lambda char: bin(int(char, 16))[2:].zfill(4), hex_input))))

    finish_cursor, decoded_output = decode_packet(0, binary_input)

    return sum([entry[0] for entry in decoded_output])


def apply_operator(operator_entry: (int, int, str, list[int]), decoded_operators: deque[(int, int, str, list[int])]):
    items = []

    if operator_entry[1] == 4:
        return int(operator_entry[2])
    else:
        for i in range(operator_entry[3][0]):
            items.append(apply_operator(decoded_operators.popleft(), decoded_operators))
        # This works fine for gt/lt/eq because Python treats True/False as 1/0 in multiplication
        return reduce(funcs[operator_entry[1]], items)


def part2():
    hex_input = get_input(16)[0]
    binary_input = ("".join(list(map(lambda char: bin(int(char, 16))[2:].zfill(4), hex_input))))

    finish_cursor, decoded_output = decode_packet(0, binary_input)

    return int(apply_operator(decoded_output.popleft(), decoded_output))
