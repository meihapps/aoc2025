from collections.abc import Callable
from functools import reduce


Range = tuple[int, int]
Ranges = list[Range]


def make_range_lambda(range: Range) -> Callable[[int], bool]:
    return lambda n: range[0] <= n <= range[1]


def make_range_funcs(ranges: Ranges):
    return list(map(make_range_lambda, ranges))


def format_input(sample: bool = False) -> tuple[Ranges, list[int]]:
    with open("sample_input.txt" if sample else "input.txt") as file:
        ranges, ids = file.read().strip().split("\n\n")

    return sorted([tuplify_range(r) for r in ranges.strip().split("\n")]), [
        int(id) for id in ids.strip().split("\n")
    ]


def tuplify_range(r: str):
    a, b = r.split("-")
    return int(a), int(b)


def part_1():
    ranges, ids = format_input()
    return len([id for id in ids if any(func(id) for func in make_range_funcs(ranges))])


def part_2():
    return sum(map(get_range_length, reduce(part_2_prime, format_input()[0], [])))


def part_2_prime(acc: Ranges, x: Range):
    return (
        [x]
        if not acc
        else acc[:-1] + [(acc[-1][0], max(acc[-1][1], x[1]))]
        if x[0] <= acc[-1][1]
        else acc + [x]
    )


def get_range_length(r: Range):
    return r[1] - r[0] + 1
