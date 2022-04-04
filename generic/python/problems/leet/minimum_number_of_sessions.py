# https://leetcode.com/problems/minimum-number-of-work-sessions-to-finish-the-tasks/
import time
from functools import lru_cache


def main():
    start_time = time.time()

    assert 1 == min_sessions([8], 8)
    assert 1 == min_sessions([0], 8)
    assert 2 == min_sessions([3, 1, 3, 1, 1], 8)
    assert 2 == min_sessions([1, 2, 3], 3)
    assert 1 == min_sessions([1, 2, 3, 4, 5], 15)
    assert 3 == min_sessions([1, 2, 3, 4, 5], 5)
    assert 2 == min_sessions([3, 9], 10)
    assert 4 == min_sessions([10, 9, 7, 1, 4, 4, 7, 2, 8, 6], 15)
    assert 7 == min_sessions([9, 9, 7, 1, 4, 4, 7, 2, 8, 6, 2, 1, 3, 7, 6, 14, 2, 1], 14)
    assert 3 == min_sessions([3, 4, 7, 8, 10], 12)

    # assert 4 == min_sessions([2, 3, 3, 4, 4, 4, 5, 6, 7, 10], 12)
    # print(min_sessions([2, 3, 3, 4, 4, 4, 5, 6, 7, 10], 12))

    print("Took {:.5f} s".format(time.time() - start_time))


# Looks like a DP task, what about some additional heuristics?
# This is not the correct solution, instead of optimizing on 'all sessions' level I did it on 'each session' level
# Quick, but not really correct for all cases
def min_sessions(tasks: list[int], session_time: int):
    memoization = {}

    def get_max_tasks(tasks: list[int], session_time: int):
        if session_time < 0:
            return -float("inf"), tasks

        if session_time == 0:
            return 0, tasks

        max_tasks_done = 0
        tasks_left = tasks

        for index, task in enumerate(tasks):
            tasks_copy = tasks.copy()
            task_value = tasks_copy.pop(index)

            if (sum(tasks), session_time) in memoization:
                return memoization[(sum(tasks), session_time)]

            tasks_done, tasks_left2 = get_max_tasks(tasks_copy, session_time - task_value)
            tasks_done += 1  # task_value done

            # Is this heuristic good enough?
            if tasks_done > max_tasks_done or (tasks_done == max_tasks_done and sum(tasks_left) > sum(tasks_left2)):
                max_tasks_done = tasks_done
                tasks_left = tasks_left2

        if (sum(tasks), session_time) not in memoization:
            memoization[(sum(tasks), session_time)] = (max_tasks_done, tasks_left)

        return max_tasks_done, tasks_left

    min_num = 0
    while tasks:
        num_of_tasks_done, tasks = get_max_tasks(tasks, session_time)
        min_num += 1
        print(f"Tasks done: {num_of_tasks_done}, Tasks left {tasks}")

    return min_num


# Solution by @DBabichev using a bitmask that solves my problem of 'not that pretty' memoization + is actually correct
def minSessions(tasks, sessionTime):
    n = len(tasks)

    @lru_cache(None)
    def dp(mask):
        if mask == 0: return (1, 0)
        ans = (float("inf"), float("inf"))
        for j in range(n):
            if mask & (1 << j):
                pieces, last = dp(mask - (1 << j))
                full = (last + tasks[j] > sessionTime)
                ans = min(ans, (pieces + full, tasks[j] + (1 - full) * last))
        return ans

    return dp((1 << n) - 1)[0]


if __name__ == "__main__":
    main()
