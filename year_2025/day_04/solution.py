def format_input(sample: bool = False):
    with open("sample_input.txt" if sample else "input.txt") as file:
        return [i for i in file.read().strip().split("\n")]


def count_neighbours(grid: list[str], x: int, y: int):
    return [
        grid[i][j]
        for i in range(x - 1, x + 2)
        for j in range(y - 1, y + 2)
        if (i, j) != (x, y) and 0 <= i < len(grid) and 0 <= j < len(grid[0])
    ].count("@")


def count_valid_rolls(grid: list[str]):
    return [cell for row in grid for cell in row].count("x")


def update_grid(grid: list[str]):
    return [
        "".join([
            "x" if grid[x][y] == "@" and count_neighbours(grid, x, y) < 4 else cell
            for y, cell in enumerate(row)
        ])
        for x, row in enumerate(grid)
    ]


def part_1():
    return count_valid_rolls(update_grid(format_input()))

def update_grid_until_unchanged(grid: list[str]):
    old_grid = []
    while old_grid != grid:
        old_grid, grid = grid, update_grid(grid)
    return grid

def part_2():
    return count_valid_rolls(update_grid_until_unchanged(format_input()))
