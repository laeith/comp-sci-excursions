graph = {
    'A': {'B', 'C'},
    'B': {'D', 'E', 'A'},
    'C': {'F', 'A'},
    'D': {'B'},
    'E': {'B', 'F'},
    'F': {'E', 'C', 'G'},
    'G': {'F'},
}


def dfs_recursive(graph, vertex, goal, path=None):  # vertex is 'start' in the first iteration
    if path is None:
        path = [vertex]
    if vertex == goal:
        return path
    else:
        for neighbor in graph[vertex] - set(path):
            return dfs_recursive(graph, neighbor, goal, path + [neighbor])


def dfs_iterative(graph, start, goal):
    stack = [(start, [start])]
    visited = {start}

    correct_paths = []

    while stack:
        (vertex, path) = stack.pop()
        for neighbor in graph[vertex] - visited:
            if neighbor == goal:
                correct_paths.append(path + [neighbor])
            elif neighbor not in visited:
                visited.add(neighbor)
                stack.append((neighbor, path + [neighbor]))

    return correct_paths


def main():
    print(dfs_iterative(graph, 'A', 'F'))
    print(dfs_recursive(graph, 'A', 'F'))


if __name__ == '__main__':
    main()
