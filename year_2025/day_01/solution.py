from functools import reduce
from itertools import accumulate


def format_input(sample: bool = False):
    with open("sample_input.txt" if sample else "input.txt") as file:
        return (
            int(line.replace("L", "-").replace("R", ""))
            for line in file.read().strip().split("\n")
        )


def part_1():
    return list(
        accumulate(format_input(), lambda a, b: (a + b) % 100, initial=50),
    ).count(0)


def part_2():
    return reduce(
        lambda state, r: (
            (state[0] + r) % 100,
            state[1]
            + (abs(state[0] + r) // 100)
            + (1 if state[0] != 0 and state[0] + r <= 0 else 0),
        ),
        format_input(),
        initial=(50, 0),
    )
