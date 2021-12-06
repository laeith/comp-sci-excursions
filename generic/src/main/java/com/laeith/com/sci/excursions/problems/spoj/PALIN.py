import random


def main():
    for _ in range(int(input())):
        x = input()
        print(process(x.strip()))


def process(line):
    smallest_palin = find_smallest_palindrome(line)
    curr_iter = get_mid_iter(line)

    while len(line) == len(smallest_palin) and ''.join(map(str, smallest_palin)) <= line:
        smallest_palin, curr_iter = advance_palin(smallest_palin, curr_iter)
    return ''.join(map(str, smallest_palin))


def find_smallest_palindrome(K: str) -> list:
    smallest_palindrome_list = list(K)
    size = len(K)
    iter = get_mid_iter(K)

    for i in range(0, iter):
        smallest_palindrome_list[size - i - 1] = smallest_palindrome_list[i]

    return smallest_palindrome_list


def get_mid_iter(input):
    return int(len(input) / 2)


def advance_palin(palin_list, i):
    # handle i < size
    size = len(palin_list)
    if i < 0:
        palin_list.insert(0, 1)
        palin_list[-1] = 1
        return palin_list, 0
    if palin_list[i] == '9':
        palin_list[i] = 0
        palin_list[size - i - 1] = 0
        return advance_palin(palin_list, i - 1)
    else:
        next_value = str(int(palin_list[i]) + 1)
        palin_list[i] = next_value
        palin_list[size - i - 1] = next_value
        return palin_list, i


def generate_random_input(size):
    randoms = []
    for i in range(0, size):
        randoms.append(random.randint(0, 9))
    if randoms[0] == 0:
        randoms[0] = 1
    return ''.join(str(x) for x in randoms)


if __name__ == "__main__":
    main()

    # assert process("0") == "1"
    # assert process("1") == "2"
    # assert process("9") == "11"
    # assert process("75") == "77"
    # assert process("99") == "101"
    # assert process("199") == "202"
    # assert process("808") == "818"
    # assert process("2133") == "2222"
    # assert process("4891") == "4994"
    # assert process("999539") == "999999"
    # assert process("79541453924626") == "79541455414597"

    # data = generate_random_input(1_000_000)
    # start = time.time()
    # process(data)
    # print(time.time() - start)

    # print("1001" < "1003")
