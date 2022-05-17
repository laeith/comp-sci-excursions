def main():
    print(combination_sum([2, 3, 6, 7], 7))

    assert combination_sum([2, 3, 6, 7], 7) == [[2, 2, 3], [7]]
    assert combination_sum([2], 1) == []


def combination_sum(candidates: list[int], target: int) -> list[list[int]]:
    valid_combinations = []
    candidates = sorted(candidates)

    def take_a_pick(combinations, curr_combination):
        if sum(curr_combination) == target:
            combinations.append(curr_combination)
            return
        elif sum(curr_combination) > target:
            return

        for possible_candidate in candidates:
            if not curr_combination or possible_candidate >= curr_combination[-1]:
                curr_combination_copy = curr_combination[:]
                curr_combination_copy.append(possible_candidate)
                take_a_pick(combinations, curr_combination_copy)

    take_a_pick(valid_combinations, [])

    return valid_combinations


if __name__ == "__main__":
    main()
