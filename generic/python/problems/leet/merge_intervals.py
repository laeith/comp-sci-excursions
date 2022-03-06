# https://leetcode.com/problems/merge-intervals/
def merge_intervals(intervals: list[list[int]]):
    intervals.sort()  # O(NLogN)

    result = []

    for interval in intervals:  # O(N)
        if len(result) == 0:
            result.append(interval)
            continue

        old_min, old_max = result[-1]
        min, max = interval

        if min <= old_max < max:
            result[-1] = [old_min, max]
        elif min > old_max:
            result.append(interval)
        else:
            # The input is within previous interval bounds, depending on sorting this check may or may not be needed
            continue

    return result


def main():
    input1 = [[1, 3], [8, 10], [15, 18], [2, 6]]
    input2 = [[1, 4], [4, 5]]
    single = [[0, 47]]

    print(merge_intervals(input1))

    assert merge_intervals(input1) == [[1, 6], [8, 10], [15, 18]]
    assert merge_intervals(input2) == [[1, 5]]
    assert merge_intervals(single) == [[0, 47]]


if __name__ == "__main__":
    main()
