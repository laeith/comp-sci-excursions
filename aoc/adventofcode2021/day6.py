from collections import deque

from utils import get_input


# TODO: Marcin: Create recursive version? Should be far cleaner and potentially more efficient

def simulate_lantern_reproduction(simulation_days: int) -> int:
    """
    :rtype:int Returns number of lanterns after provided number of days
    """

    data = get_input(6, int, sep=",")

    days_left = simulation_days

    new_cycle_time = 8
    old_cycle_time = 6

    reproduction_queue = deque()
    reproduction_queue.extend([0 for _ in range(new_cycle_time + 1)])

    for lantern_internal_timer in data:
        reproduction_queue[lantern_internal_timer] = reproduction_queue[lantern_internal_timer] + 1

    while days_left > 0:
        reproducing_lanterns = reproduction_queue.popleft()

        reproduction_queue.append(reproducing_lanterns)
        reproduction_queue[old_cycle_time] = reproduction_queue[old_cycle_time] + reproducing_lanterns

        days_left -= 1

    return sum(reproduction_queue)


def part1():
    return simulate_lantern_reproduction(80)


def part2():
    # Well, doing it in Python has it upsides, doesn't it?
    return simulate_lantern_reproduction(256)
