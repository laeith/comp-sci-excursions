import importlib

if __name__ == "__main__":
    print("Advent of Code 2021 solutions:")
    for day_num in range(1, 26):
        for part_id in (1, 2):
            try:
                day = importlib.import_module(f'day{day_num}')
                solution = getattr(day, f'part{part_id}')
                print(f'Day {day_num} Part {part_id}: {solution()}')
            except (ModuleNotFoundError, AttributeError):
                print(f'Day {day_num} Part {part_id} solution is not available')
