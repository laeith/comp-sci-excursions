from utils import get_input


def parse_input(data: list[str]) -> (list[(int, int)], list[(str, int)]):
    """
    Returns points and folds following example:
    points = [(1,0), (12,11)]
    folds = [('x', 7), ('y', 28)]
    """
    points = set([(int(point.split(",")[0]), (int(point.split(",")[1]))) for point in data
                  if len(point) > 0 and point[0].isdigit()])
    folds = [(point.split("=")[0][-1], int(point.split("=")[1])) for point in data if point.startswith("fold")]
    return points, folds


def fold(axis: str, folding_val: int, points: set[(int, int)]) -> set[(int, int)]:
    match axis:
        case "x":
            folded_points = [(folding_val - (point[0] - folding_val), point[1]) for point in points
                             if point[0] > folding_val]
            points = set([point for point in points if point[0] < folding_val] + folded_points)
        case "y":
            folded_points = [(point[0], folding_val - (point[1] - folding_val)) for point in points
                             if point[1] > folding_val]
            points = set([point for point in points if point[1] < folding_val] + folded_points)
        case _:
            print(f"Should not happen, can't fold against: {axis}")

    return points


def part1():
    points, folds = parse_input(get_input(13))

    initial_fold = folds[0]
    points = fold(initial_fold[0], initial_fold[1], points)

    return len(points)


def pretty_print(points: set[(int, int)]) -> None:
    max_x = max(point[0] for point in points)
    max_y = max(point[1] for point in points)

    grid = [["-" for _ in range(max_x + 1)] for _ in range(max_y + 1)]

    for point in points: grid[point[1]][point[0]] = "X"
    for row in grid:
        print(''.join(row))


def part2():
    points, folds = parse_input(get_input(13))

    for folding in folds:
        points = fold(folding[0], folding[1], points)

    # Uncomment to see where I got the answer from:
    # pretty_print(points)

    return "LRFJBJEH"
