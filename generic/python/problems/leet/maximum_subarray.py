# https://leetcode.com/problems/maximum-subarray/


def main():
    assert 6 == max_sub_array([-2, 1, -3, 4, -1, 2, 1, -5, 4])
    assert 1 == max_sub_array([1])
    assert 23 == max_sub_array([5, 4, -1, 7, 8])
    assert -20 == max_sub_array([-20])
    assert 3 == max_sub_array([2, -1, 2])
    assert -1 == max_sub_array([-2, -1, -10])

    assert 6 == max_sub_array_carry([-2, 1, -3, 4, -1, 2, 1, -5, 4])
    assert 1 == max_sub_array_carry([1])
    assert 23 == max_sub_array_carry([5, 4, -1, 7, 8])
    assert -20 == max_sub_array_carry([-20])
    assert 3 == max_sub_array_carry([2, -1, 2])
    assert -1 == max_sub_array_carry([-2, -1, -10])

    assert 6 == max_sub_array_bf([-2, 1, -3, 4, -1, 2, 1, -5, 4])
    assert 1 == max_sub_array_bf([1])
    assert 23 == max_sub_array_bf([5, 4, -1, 7, 8])
    assert -20 == max_sub_array_bf([-20])
    assert 3 == max_sub_array_bf([2, -1, 2])
    assert -1 == max_sub_array_bf([-2, -1, -10])


# O(n)
def max_sub_array(nums: list[int]) -> int:
    if len(nums) == 1:
        return nums[0]

    max_sum = nums[0]
    curr_sum = nums[0]

    for i in range(1, len(nums)):
        if curr_sum > 0:
            curr_sum += nums[i]
        else:
            curr_sum = nums[i]

        if curr_sum > max_sum:
            max_sum = curr_sum

    return max_sum


# More concise version with in-place changes -> still O(n)
def max_sub_array_carry(nums: list[int]) -> int:
    for i in range(1, len(nums)):
        if nums[i - 1] > 0:
            nums[i] += nums[i - 1]
    return max(nums)


# Brute force -> Generate all combinations and check them -> very slow O(n^2)
def max_sub_array_bf(nums: list[int]) -> int:
    max_sum = nums[0]
    for i in range(0, len(nums)):
        for k in range(i + 1, len(nums) + 1):
            if sum(nums[i:k]) > max_sum:
                max_sum = sum(nums[i:k])
    return max_sum


if __name__ == "__main__":
    main()
