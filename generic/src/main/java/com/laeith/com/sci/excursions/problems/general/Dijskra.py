graph = {
    'A': {('B', 1), ('C', 0)},
    'B': {('D', 1), ('E', 5), ('A', 1)},
    'C': {('F', 299), ('A', 0)},
    'D': {('B', 1)},
    'E': {('B', 5), ('F', 1)},
    'F': {('E', 1), ('C', 2), ('G', 20)},
    'G': {('F', 20)},
}

inf = float('inf')


def dijkstra(graph, start, destination):
    visited = {start}
    unvisited = graph.copy()  # copy graph

    min_distance_map = {key: inf for key in graph}
    min_distance_map[start] = 0

    prev = {key: None for key in graph}  # no previous vertexes at start

    while unvisited:
        curr_vert = min(unvisited.keys(), key=lambda vertex: min_distance_map[vertex])
        del unvisited[curr_vert]
        visited.add(curr_vert)

        if min_distance_map[curr_vert] == inf:  # nope
            break

        for vert in graph[curr_vert]:
            dist = min_distance_map[curr_vert] + vert[1]
            if dist < min_distance_map[vert[0]]:
                min_distance_map[vert[0]] = dist
                prev[vert[0]] = curr_vert

        if destination in visited:  # destination already found
            path = []
            vertex = curr_vert
            while vertex is not None:  # reverse the steps to
                path.append(vertex)
                vertex = prev[vertex]

            path.reverse()

            return path


if __name__ == '__main__':
    print(dijkstra(graph, 'A', 'F'))
