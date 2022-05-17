def main():
    print(combination_sum([10, 1, 2, 7, 6, 1, 5], 8))

    # Glorious python randomization
    assert sorted(combination_sum([10, 1, 2, 7, 6, 1, 5], 8)) == [[1, 1, 6], [1, 2, 5], [1, 7], [2, 6]]
    assert sorted(combination_sum([2, 5, 2, 1, 2], 5)) == [[1, 2, 2], [5]]
    assert sorted(combination_sum([2, 5, 2, 2], 1)) == []
    assert sorted(combination_sum([1, 2], 4)) == []

    # Very unfriendly test-case
    assert sorted(
        combination_sum([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 27)) == []


def combination_sum(candidates: list[int], target: int) -> list[list[int]]:
    valid_combinations = []
    candidates.sort()

    def take_a_pick(combinations, original_candidates, curr_combination, position):
        if sum(curr_combination) == target:
            combinations.append(curr_combination)
            return
        elif sum(curr_combination) > target:
            return

        # Position is only introduced so that we don't have to keep copying the original_candidates needlessly
        for index in range(position, len(original_candidates)):
            # Hmmm
            if index > position and original_candidates[index] == original_candidates[index - 1]:
                continue

            if original_candidates[index] > target:
                break

            curr_combination_copy = curr_combination[:]
            curr_combination_copy.append(original_candidates[index])

            take_a_pick(combinations, original_candidates, curr_combination_copy, index + 1)

    take_a_pick(valid_combinations, candidates, [], 0)

    return valid_combinations


if __name__ == "__main__":
    main()
