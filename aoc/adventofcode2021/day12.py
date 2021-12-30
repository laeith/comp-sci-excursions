from utils import get_input


def build_graph(vertices: list[tuple[str, str]]):
    graph = {}

    for vertex in vertices:
        if vertex[0] in graph:
            graph[vertex[0]].append(vertex[1])
        else:
            graph[vertex[0]] = [vertex[1]]

        if vertex[1] in graph:
            graph[vertex[1]].append(vertex[0])
        else:
            graph[vertex[1]] = [vertex[0]]

    return graph


# TODO: Marcin: Can be reworked to strategy pattern

# 3421
def part1():
    graph = build_graph(get_input(12, lambda line: line.split("-")))

    def find_all_paths(current: str, visited: list[str] = [], curr_path: list[str] = [],
                       paths_found: list[list[str]] = []):
        if current.islower():
            visited.append(current)
        curr_path.append(current)

        if current == 'end':
            paths_found.append(curr_path)
            return

        for neighbour in graph[current]:
            if neighbour not in visited:
                find_all_paths(neighbour, visited[:], curr_path[:], paths_found)

        return paths_found

    paths = find_all_paths('start')

    return len(paths)


# 84870
def part2():
    graph = build_graph(get_input(12, lambda line: line.split("-")))

    def find_all_paths(current: str, visited: list[str] = [], curr_path: list[str] = [],
                       paths_found: list[list[str]] = [],
                       was_small_cave_visited_twice: bool = False):
        if current.islower():
            visited.append(current)
        curr_path.append(current)

        if current == 'end':
            paths_found.append(curr_path)
            return

        for neighbour in graph[current]:
            if neighbour not in visited:
                find_all_paths(neighbour, visited[:], curr_path[:], paths_found, was_small_cave_visited_twice)
            if neighbour in visited and not was_small_cave_visited_twice and neighbour not in ['end', 'start']:
                find_all_paths(neighbour, visited[:], curr_path[:], paths_found, True)

        return paths_found

    paths = find_all_paths('start')

    return len(paths)
