# day 3: lobby

this puzzle is about finding the highest number you can produce with a pre-existing number by keeping a specific number of digits in order.
for example, say i have this number and can keep 2 digits:

```
818181911112111
```

i would pick the 9 and the 2 to make 92. i couldn't pick the 9 and the 8 to make 98 because after the 9 there are no more 8s, and i wouldn't pick the 8 over the 9 because any number in the 90s is bigger than any number in the 80s.

## formatting

```python
with open("sample_input.txt" if sample else "input.txt") as file:
    return (list(map(int, line)) for line in file.read().strip().split("\n"))
```

here we're just taking each line in the file, and mapping int to them to get a list of integer digits for each line.


## both parts

for part 1 we get to pick 2 digits, and for part 2 we get to pick 12. this being the only difference between them, we can make a function that's number agnostic and just use it for both.

the general flow here is quite intuitive. if we want n digits, and we've got i digits so far, we can't pick a digit from the last `n - i - 1` digits. this is because we won't have enough digits left to finish off our number otherwise.

if we've taken a digit from position n, we also can't take a digit from the first n digits. otherwise we could end up using digits out of order.

once we know the range we can take from, we have to decide on how to choose from that range. in this case we want the earliest instance of the highest number in that range.

```py
(index := max(range(len(l)), key=l.__getitem__), l[index])
```

as you can see we're returning both the index and the value here rather than just the value. this is because without the index we can't narrow the problem scope properly. also a fun little use of dunders in sorting!

while the rest is sort of just one step, this is split into 2 functions because part of that step looks icky and i want it to not infect anything else.

```py
def get_best_joltage_helper(bank: list[int], batteries: int):
    last_index = -1
    for i in reversed(range(batteries)):
        index, m = find_max_with_index(bank[last_index + 1 : len(bank) - i])
        last_index += index + 1
        yield m


def get_best_joltage(bank: list[int], batteries: int):
    return int("".join(map(str, get_best_joltage_helper(bank, batteries))))
```

this is keeping track of the current problem space so that `find_max_with_index` can do it's thing effectively.
then it gets the digits we've chosen, string concatenates them and turns it into a number.

all that remains is the runner for each part. very simple, just saying 2 digits for part 1 and 12 for part 2.

```py
sum(get_best_joltage(bank, 2) for bank in format_input())
sum(get_best_joltage(bank, 12) for bank in format_input())
```
