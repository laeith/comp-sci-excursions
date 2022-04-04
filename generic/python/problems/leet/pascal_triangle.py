# https://leetcode.com/problems/pascals-triangle/

def main():
    print(pascal_triangle(6))

    assert [[1]] == pascal_triangle(1)
    assert [[1], [1, 1]] == pascal_triangle(2)
    assert [[1], [1, 1], [1, 2, 1]] == pascal_triangle(3)
    assert [[1], [1, 1], [1, 2, 1], [1, 3, 3, 1], [1, 4, 6, 4, 1]] == pascal_triangle(5)

    assert [[1]] == pascal_triangle_alternative(1)
    assert [[1], [1, 1]] == pascal_triangle_alternative(2)
    assert [[1], [1, 1], [1, 2, 1]] == pascal_triangle_alternative(3)
    assert [[1], [1, 1], [1, 2, 1], [1, 3, 3, 1], [1, 4, 6, 4, 1]] == pascal_triangle_alternative(5)


def pascal_triangle(num_rows: int) -> list[list[int]]:
    generated = []

    def generate_num(n):
        if n == 1:
            new = [1]
        else:
            previous = generate_num(n - 1)

            new = []
            new.append(1)
            for i in range(0, len(previous) - 1):
                new.append(previous[i] + previous[i + 1])
            new.append(1)

        generated.append(new)
        return new

    generate_num(num_rows)
    return generated


# With Python magic
def pascal_triangle_alternative(num_rows):
    ret = [[1]]

    for _ in range(num_rows):
        ret.append([a + b for a, b in zip([0] + ret[-1], ret[-1] + [0])])

    return ret[:num_rows]


if __name__ == "__main__":
    main()
