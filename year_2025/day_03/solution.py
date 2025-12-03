def format_input(sample: bool = False):
    with open("sample_input.txt" if sample else "input.txt") as file:
        return (list(map(int, line)) for line in file.read().strip().split("\n"))


def find_max_with_index(l: list[int]):
    return (index := max(range(len(l)), key=l.__getitem__), l[index])


def get_best_joltage_helper(bank: list[int], batteries: int):
    last_index = -1
    for i in reversed(range(batteries)):
        index, m = find_max_with_index(bank[last_index + 1 : len(bank) - i])
        last_index += index + 1
        yield m


def get_best_joltage(bank: list[int], batteries: int):
    return int("".join(map(str, get_best_joltage_helper(bank, batteries))))


def part_1():
    return sum(get_best_joltage(bank, 2) for bank in format_input())


def part_2():
    return sum(get_best_joltage(bank, 12) for bank in format_input())
