from functools import reduce
from itertools import accumulate

"""
part 1
"""
with open("01.txt") as file:
    rotations = (
        int(line.replace("L", "-").replace("R", ""))
        for line in file.read().strip().split("\n")
    )

result = list(
    accumulate(rotations, lambda a, b: (a + b) % 100, initial=50),
).count(0)
print(result)

"""
part 2
"""
with open("01.txt") as file:
    rotations = (
        int(line.replace("L", "-").replace("R", ""))
        for line in file.read().strip().split("\n")
    )

result = reduce(
    lambda state, r: (
        (state[0] + r) % 100,
        state[1]
        + (abs(state[0] + r) // 100)
        + (1 if state[0] != 0 and state[0] + r <= 0 else 0),
    ),
    rotations,
    initial=(50, 0),
)

print(result)
