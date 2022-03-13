from utils import get_input, Point, get_neighbors_9_including


def part1():
    return execute_simulation(2)


def part2():
    return execute_simulation(50)


def get_algo_index(point: Point, lights: set[Point], simulation_step: int, max_x, min_x, max_y, min_y) -> int:
    def point_to_light(inner_point: Point):
        x, y = inner_point
        if x <= min_x or x >= max_x or y <= min_y or y >= max_y:
            return '1'
        elif inner_point in lights:
            return '1'
        else:
            return '0'

    points = get_neighbors_9_including(point)

    # This is because 'background' is actually alternating between being lit and dark due to '#' on index 0 and . on
    # the final index in the decoding algorithm from day 20 input
    if simulation_step % 2 != 0:
        binary = list(map(point_to_light, points))
    else:
        binary = list(map(lambda point: '1' if point in lights else '0', points))

    return int(''.join(binary), 2)


def execute_simulation(num_of_steps: int) -> int:
    data = get_input(20)

    algorithm = data[0]
    input_image = data[2:]

    # Infinite Grid, let's store only 'lights' - #
    lights = set()

    for y, row in enumerate(input_image):
        for x, pixel in enumerate(row):
            if pixel == '#': lights.add((x, y))

    max_x, max_y = len(input_image), len(input_image[0])
    min_x, min_y = 0, 0

    simulation_step = 0
    while simulation_step < num_of_steps:
        new_lights = set()

        max_x += 1
        max_y += 1
        min_x -= 1
        min_y -= 1

        for x in range(min_x, max_x + 1):
            for y in range(min_y, max_y + 1):
                index = get_algo_index((x, y), lights, simulation_step, max_x, min_x, max_y, min_y)
                if algorithm[index] == "#": new_lights.add((x, y))

        lights = new_lights
        simulation_step += 1

    return len(lights)


# util function to see the image lit by points (size is manually adjusted)
def pretty_print(lights: set[Point]):
    out = ""
    for y in range(-7, 16):
        for x in range(-7, 16):
            if (x, y) in lights:
                out = out + "#"
            else:
                out = out + "."
        out = out + "\n"

    print(out)
