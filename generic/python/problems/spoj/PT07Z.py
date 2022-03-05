import copy

from _collections import deque

graph = {}


def main():
    num_of_nodes = input().strip()  # 0 < N <= 10000

    for _ in range(int(num_of_nodes) - 1):
        node_pair_str = input().strip().split(" ")
        build_connection(node_pair_str[0], node_pair_str[1])

    # print(graph)
    longest_first_iteration = get_longest_path(graph)  # 7
    # print(longest_first_iteration)
    furthest_node = longest_first_iteration.pop()
    # print(furthest_node)
    actually_longest_path = get_longest_path(graph, furthest_node)
    # print(actually_longest_path)
    print(len(actually_longest_path) - 1)


def get_longest_path(graph: dict, starting_node: str = None) -> deque:
    if starting_node is None:
        starting_node = list(graph.keys())[0]

    start_path = deque()

    longest_path = get_longest_path_recursive(starting_node, start_path, deque())

    return longest_path


def get_longest_path_iteratively(graph: dict) -> deque:
    nodes = list(graph.keys())
    longest_path = deque()

    unvisited = deque()
    unvisited.append((deque(), nodes[0]))

    while len(unvisited) != 0:
        curr_path, next_node = unvisited.pop()
        if next_node not in curr_path:
            curr_path.add(next_node)
            if len(graph[next_node]) != 0:  # add all neighbours
                for neighbour in graph[next_node]:
                    unvisited.append((copy.copy(curr_path), neighbour))
            else:
                if len(curr_path) > longest_path:
                    longest_path = curr_path
        else:
            continue

    return longest_path


def get_longest_path_recursive(curr_node: str, curr_path: deque, longest_path: deque) -> deque:
    curr_path.append(curr_node)

    # because it's a undirected graph (or at least we treat is as such)
    if len(graph[curr_node]) != 1 or graph[curr_node][0] not in curr_path:
        for node in graph[curr_node]:
            if node not in curr_path:  # avoid cycles
                longest_path = get_longest_path_recursive(node, curr_path, longest_path)
    else:
        if len(longest_path) < len(curr_path):
            longest_path = copy.copy(curr_path)
    curr_path.pop()
    return longest_path


def build_connection(node1, node2) -> None:
    if node1 in graph:
        graph[node1].append(node2)
    else:
        graph[node1] = [node2]

    if node2 in graph:
        graph[node2].append(node1)
    else:
        graph[node2] = [node1]


if __name__ == "__main__":
    main()
