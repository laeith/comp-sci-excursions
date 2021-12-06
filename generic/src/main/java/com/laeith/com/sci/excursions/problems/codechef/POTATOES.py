def sieve_of_eratosthenes(max_num: int) -> list:
    sieve = [(x, True) for x in range(0, max_num + 1)]
    for i in range(2, len(sieve)):
        item = sieve[i]
        if item[1] is True:
            p = out = item[0]
            out += p
            while out <= max_num:
                sieve[out] = (out, False)
                out += p
    return sieve


def find_nearest_prime(num: int, sieve: list) -> int:
    for i in range(num + 1, len(sieve)):
        if sieve[i][1] is True: return sieve[i][0]


if __name__ == '__main__':
    SIEVE = sieve_of_eratosthenes(2003)
    num_test_cases = int(input())
    for _ in range(0, num_test_cases):
        field1, field2 = map(int, input().split(" "))
        potats = field1 + field2
        print(find_nearest_prime(potats, SIEVE) - potats)
