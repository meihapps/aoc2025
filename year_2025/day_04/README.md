# day 4 - printing department

this puzzle takes place on a 2d grid, with paper rolls placed on it. you need to find pieces of paper that don't have more than 4 adjacent pieces of paper (including diagonals).

for formatting the input we'll be turning it into a list of strings. in any other language i'd do a list of characters but python doesn't have characters. strings are normally just lists of characters anyway so it's not much different, key differences are just that strings are immutable and lists are not but that shouldn't be a problem here.

```py
with open("sample_input.txt" if sample else "input.txt") as file:
    return [i for i in file.read().strip().split("\n")]
```

## part 1

the main steps here are:
- counting cell neighbours
- updating the grid based on that information
- counting how many rolls were valid

### counting cell neighbours

```py
def count_neighbours(grid: list[str], x: int, y: int):
    return [
        grid[i][j]
        for i in range(x - 1, x + 2)
        for j in range(y - 1, y + 2)
        if (i, j) != (x, y) and 0 <= i < len(grid) and 0 <= j < len(grid[0])
        ].count("@")
    ]
```

this is just exploring the square around the cell. the conditionals listed are:
- we dont want to check the cell in the centre (it isn't its own neighbour)
- we dont want to check x values that are off grid
- we dont want to check y values that are off grid

counting @s is the easiest way to go about it.

### updating the grid

```py
def update_grid(grid: list[str]):
    return [
        "".join([
            "x" if grid[x][y] == "@" and count_neighbours(grid, x, y) < 4 else cell
            for y, cell in enumerate(row)
        ])
        for x, row in enumerate(grid)
    ]
```

here we are going through each of the cells and if there is a roll and the neighbour requirement are both met, we just replace that cell with an "x". this is so that we don't have to keep track of how many rolls have been removed from the grid - that information is maintained.

### counting valid rolls

```py
def count_valid_rolls(grid: list[str]):
    return [cell for row in grid for cell in row].count("x")
```
now we just count how many "x"s are on the grid.

## part 2

much the same, but now we treat all of those "x"s as removed rolls, so that we can do multiple passes to find the maximum number of removable rolls.

unfortunately there doesn't seem to be a nice heuristic for being "done", so i'm just going to track the last state of the grid and the current state of the grid. if they are the same you know the last pass put it in an end state.

```py
def update_grid_until_unchanged(grid: list[str]):
    old_grid = []
    while old_grid != grid:
        old_grid, grid = grid, update_grid(grid)
    return grid
```
