from problems.utils import create_new_grid


def main():
    assert 3 == unique_paths_bf(3, 2)
    assert 28 == unique_paths_bf(3, 7)


# Oooo... robot can only move down or right...
def unique_paths_bf(m, n):
    start = (0, 0)
    end = (n - 1, m - 1)

    grid = create_new_grid(n, m, 0)

    def calculate_unique_paths(point):
        if point not in grid:
            return 0

        # Each visits upticks 'paths' count
        grid[point] = grid[point] + 1

        # This is quite inefficient given that it may visit the same point multiple times
        calculate_unique_paths((point[0] - 1, point[1]))
        calculate_unique_paths((point[0], point[1] - 1))

    calculate_unique_paths(end)
    return grid[start]


def unique_paths(m, n):
    rows = [[1 for _ in range(n)] for _ in range(m)]

    for i in range(1, m):
        for j in range(1, n):
            rows[i][j] = rows[i][j - 1] + rows[i - 1][j]

    return rows[-1][-1]


if __name__ == "__main__":
    main()
