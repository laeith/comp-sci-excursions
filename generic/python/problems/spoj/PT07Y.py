from _collections import deque

graph = {}


# look for cycle
# look if all visited
def main():
    num_of_nodes, num_of_edges = input().strip().split(" ")  # 0 < N <= 10000

    # graph = {x: [] for x in range(1, int(num_of_nodes) + 1)}
    for i in range(1, int(num_of_nodes) + 1):
        graph[i] = []

    # print(graph)

    for _ in range(int(num_of_edges)):
        node_pair_str = input().strip().split(" ")
        build_connection(int(node_pair_str[0]), int(node_pair_str[1]))

    # print(graph)

    if is_tree(graph):
        print("YES")
    else:
        print("NO")


def is_tree(graph: dict) -> bool:
    starting_node = list(graph.keys())[0]  # any node will do

    visited = set()
    unvisited = deque()

    unvisited.append(starting_node)

    paths_taken = set()

    while len(unvisited) != 0:
        curr_node = unvisited.pop()

        if curr_node in visited:
            return False  # cycle detected

        visited.add(curr_node)

        for node in graph[curr_node]:
            if (node, curr_node) not in paths_taken:
                paths_taken.add((curr_node, node))
                unvisited.append(node)

    all_nodes = set(graph.keys())

    return visited == all_nodes  # did we visit all nodes?


def build_connection(node1: int, node2: int) -> None:
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
