# https://leetcode.com/problems/queue-reconstruction-by-height
# 1 - brute force - get all possible combinations and check them... obviously won't work for N = 2000, probably even with optimizations
# 2 - sort them cleverly from highest to lowest
from collections import deque


def main():
    print(reconstruct_queue([[7, 0], [4, 4], [7, 1], [5, 0], [6, 1], [5, 2]]))

    assert reconstruct_queue([[7, 0], [4, 4], [7, 1], [5, 0], [6, 1], [5, 2]]) == [[5, 0], [7, 0], [5, 2], [6, 1],
                                                                                   [4, 4], [7, 1]]
    assert reconstruct_queue([[6, 0], [5, 0], [4, 0], [3, 2], [2, 2], [1, 4]]) == [[4, 0], [5, 0], [2, 2], [3, 2],
                                                                                   [1, 4], [6, 0]]
    assert reconstruct_queue([[9, 0], [7, 0], [1, 9], [3, 0], [2, 7], [5, 3], [6, 0], [3, 4], [6, 2], [5, 2]]) == [
        [3, 0], [6, 0], [7, 0], [5, 2], [3, 4], [5, 3], [6, 2], [2, 7], [9, 0], [1, 9]]

    assert reconstruct_queue([[8, 2], [4, 2], [4, 5], [2, 0], [7, 2], [1, 4], [9, 1], [3, 1], [9, 0], [1, 0]]) == [
        [1, 0], [2, 0], [9, 0], [3, 1], [1, 4], [9, 1], [4, 2], [7, 2], [8, 2], [4, 5]]


def reconstruct_queue(people: list[list[int]]) -> list[list[int]]:
    people = deque(sorted(people))  # python's list would be terrible for removals

    result = []

    while people:
        highest = people[-1][0]

        top_picks = []
        while people and (people[-1][0] == highest):
            top_picks.append(people.pop())

        top_picks.sort()

        for pep in top_picks:
            result.insert(pep[1], pep)

    return result


if __name__ == "__main__":
    main()
