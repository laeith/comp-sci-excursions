# https://leetcode.com/problems/spiral-matrix-ii/
def main():
    input1 = 3
    input2 = 1

    print(get_spiral(input1))
    print(get_spiral(input2))
    print(get_spiral(4))

    assert get_spiral(input1) == [[1, 2, 3], [8, 9, 4], [7, 6, 5]]
    assert get_spiral(input2) == [[1]]
    assert get_spiral(4) == [[1, 2, 3, 4], [12, 13, 14, 5], [11, 16, 15, 6], [10, 9, 8, 7]]


# 1 <= n <= 20
def get_spiral(n: int) -> list[list[int]]:
    # Prepopulate so that it's cleaner later on
    result = [[0 for _ in range(n)] for _ in range(n)]

    curr_number = 1
    for i in range(n):
        result[0][i] = curr_number
        curr_number += 1

    x, y = n - 1, 0

    while abs(n) > 1:
        direction = n // abs(n)
        for _ in range(abs(n) - 1):
            y += direction
            result[y][x] = curr_number
            curr_number += 1

        for _ in range(abs(n) - 1):
            x -= direction
            result[y][x] = curr_number
            curr_number += 1

        n = -1 * (n - direction)

    return result


if __name__ == "__main__":
    main()
