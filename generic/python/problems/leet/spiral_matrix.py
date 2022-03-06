# https://leetcode.com/problems/spiral-matrix/
def main():
    input1 = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    input2 = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]
    single = [[-18]]

    print(get_spiral(input1))
    print(get_spiral(input2))
    print(get_spiral(single))

    assert get_spiral(input1) == [1, 2, 3, 6, 9, 8, 7, 4, 5]
    assert get_spiral(input2) == [1, 2, 3, 4, 8, 12, 11, 10, 9, 5, 6, 7]
    assert get_spiral(single) == [-18]


# Alternatively, we could make the first row move manually and then write a simple algorithm for a decreasing L move
def get_spiral(matrix: list[list[int]]) -> list[int]:
    x_len, y_len = len(matrix[0]), len(matrix)

    x, y = 0, 0
    result = []
    visited = set()

    result.append(matrix[y][x])
    visited.add((x, y))

    all_items_num = x_len * y_len
    while len(visited) < all_items_num:
        for dx in range(0, abs(x_len) - 1):
            if (x + x_len // abs(x_len), y) in visited:
                break
            else:
                x += x_len // abs(x_len)  # how to get a signed 1?
                visited.add((x, y))
                result.append(matrix[y][x])

        for dy in range(0, abs(y_len) - 1):
            if (x, y + y_len // abs(y_len)) in visited:
                break
            else:
                y += y_len // abs(y_len)
                visited.add((x, y))
                result.append(matrix[y][x])

        x_len = -1 * x_len
        y_len = -1 * y_len

    return result


if __name__ == "__main__":
    main()
