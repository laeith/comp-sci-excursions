from adventofcode2021.utils import get_input, get_ints


# We might need to switch to 'ranges' instead of actual cubics to make it work
def is_valid(min_x, max_x):
    return -50 <= min_x <= 50 or -50 <= max_x <= 50


def part1():
    data = get_input(22, lambda line: line.split(" "))

    cuboids = set()

    for step in data:
        switch = step[0]
        min_x, max_x, min_y, max_y, min_z, max_z = map(int, get_ints(step[1]))
        if is_valid(min_x, max_x) and is_valid(min_y, max_y) and is_valid(min_z, max_z):
            min_x, max_x = limit(min_x, max_x)
            min_y, max_y = limit(min_y, max_y)
            min_z, max_z = limit(min_z, max_z)
        else:
            continue

        # print(f"Processing {switch}:\t x: {min_x}:{max_x} y: {min_y}:{max_y} z: {min_z}:{max_z}")

        for x in range(min_x, max_x + 1):
            for y in range(min_y, max_y + 1):
                for z in range(min_z, max_z + 1):
                    if switch == "on":
                        cuboids.add((x, y, z))
                    else:
                        cuboids.discard((x, y, z))

    return len(cuboids)


def limit(min_coord, max_coord):
    return max([-50, min_coord]), min([50, max_coord])


# Obviously the initial approach is not going to work for that type of input...
# I should move to range-based calculations
def part2():
    # data = get_input(22, lambda line: line.split(" "))
    #
    # for step in data:
    #     switch = step[0]
    #     min_x, max_x, min_y, max_y, min_z, max_z = map(int, get_ints(step[1]))
    pass
