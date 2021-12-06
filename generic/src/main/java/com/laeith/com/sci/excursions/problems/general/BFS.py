from queue import Queue

graph = {
    'A': {'B', 'C'},
    'B': {'D', 'E', 'A'},
    'C': {'F', 'A'},
    'D': {'B'},
    'E': {'B', 'F'},
    'F': {'E', 'C', 'G'},
    'G': {'F'},
}


def bfs_iterative(graph, start, goal):
    visited = set()

    fifo_queue = Queue()
    fifo_queue.put((start, [start]))

    while fifo_queue:
        (vertex, path) = fifo_queue.get()
        for neighbor in graph[vertex] - visited:
            if neighbor == goal:
                return path + [neighbor]
            elif neighbor not in visited:
                visited.add(neighbor)
                fifo_queue.put((neighbor, path + [neighbor]))

    return None


if __name__ == '__main__':
    print(bfs_iterative(graph, 'A', 'F'))
