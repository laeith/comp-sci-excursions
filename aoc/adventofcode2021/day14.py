from collections import Counter

from utils import get_input


# Initially done with a naive approach with actual full-blown simulation - i.e. adding and modifying a mutable list
# but because lists are backed by Arrays in Python insertion in the middle is very, very expensive (was taking ~99.9%
# of computation). It worked for the part 1 but failed miserable for part 2.
# I believe a proper linked list (with in-place modifications) could potentially improve the situation but we don't have
# such structure readily available in Python (?), even if the actual LL implementation is relatively easy I eventually
# switched to the pair counting method, which is probably the fastest out of the 3 approaches mentioned here.

def simulate_step(pairs_counter: Counter, mappings: dict[str:str]) -> Counter:
    temp_counter = Counter()
    for pair, count in pairs_counter.items():
        temp_counter[pair[0] + mappings[pair]] += count
        temp_counter[mappings[pair] + pair[1]] += count
        temp_counter[pair] -= count

    return pairs_counter + temp_counter


def polymer_to_counter(polymer: str):
    elements = list(polymer)
    counter = Counter()

    for i in range(1, len(elements)):
        pair = elements[i - 1] + elements[i]
        counter[pair] += 1

    return counter


def run_simulation(num_of_steps: int) -> int:
    polymer, _, *rules = get_input(14)
    mappings = dict(r.split(" -> ") for r in rules)

    pairs_counter = polymer_to_counter(polymer)

    for i in range(num_of_steps):
        pairs_counter = simulate_step(pairs_counter, mappings)

    elements_counter = count_elements(pairs_counter, polymer)

    return max(elements_counter.values()) - min(elements_counter.values())


def count_elements(pairs_counter, polymer):
    elements_counter = Counter()
    # Because I keep only pairs of elements in the counter, elements are actually doubled as they almost always
    # appear in both adjacent pairs, e.g. in 'ABC' we get 'AB' and 'BC' so 'B' is counted twice despite being present
    # only once. To remedy that I count only the first element in a pair (including the first polymer element)
    for pair, count in pairs_counter.items():
        elements_counter[pair[0]] += count
    # it works but omits the final element, which will always be the same as in the initial polymer template
    # thus the addition
    elements_counter[polymer[-1]] += 1
    return elements_counter


# 3697
def part1():
    return run_simulation(10)


# 4371307836157
def part2():
    return run_simulation(40)
