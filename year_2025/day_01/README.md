# day 1: secret entrance

the basic premise here is that we need a password to get through a door. we have a dial and a list of rotations. how the password is found is different for part 1 and part 2.
we're given the rotations as line-separated values in the format "[lr]\d+" which is cool and all but definitely not the easiest way to work with them.

to make this easier to work around, we'll reformat them like so:
```py
with open("01.txt") as file:
    rotations = (
        int(line.replace("l", "-").replace("r", ""))
        for line in file.read().strip().split("\n")
    )
```

with this, we now have a list of numbers representing the rotations. negative numbers for left rotations and positive numbers for right rotations.


## part 1

the way we find the password here is by applying the rotations to the dial and seeing how many times the dial lands on 0.
this is quite simple, as we can just accumulate the list with addition modulo 100, starting at 50, and count the 0s.

```py
result = list(
    accumulate(rotations, lambda a, b: (a + b) % 100, initial=50),
).count(0)
```

## part 2

part 2 is a bit more involved. now, instead of just counting how many times it lands on 0 we have to count how many times it lands on OR passes through 0.

essentially, this boils down to a few main cases:

- the rotation will bring it above 100
- the rotation will bring it below 0
- the rotation will bring it to 0/100 (same value)
- the rotation started on 0 and then went left (special case!! annoying!! messes everything up!!)

### >100

in this instance, we can cleanly use `(current_value + rotation) // 100` to find out how many "zeros" to add.
we're using integer division here to cover for cases where it goes past 0 multiple times in a single rotation.

### <0

here we can pretty easily see that this mirrors the above 100 case. if we go below zero, it acts exactly as if we went above 100 by the same amount.
so for this we'd use something like `(-(current_value + rotation) // 100) + 1`. lets break that down a little further.

why the negative?
-5 modulo 100 is 95 modulo 100, not 5 modulo 100. we want it to be acting the same as 5 so that it's mirroring the above 100 case.

why the `+ 1`?
we want our `<0` case to map perfectly to our `>100` case. simply flipping the sign isn't enough to handle the fact that those numbers are all 100 higher. i could have instead done a `+ 100` before the `// 100` but a `+ 1` after feels cleaner to me.

### 0/100

in this case we would just want to add 1. landing on a zero counts as 1.

### starting on 0 and rotating left

this can cause some problems. if we start on 0 and go left, that 0 gets counted twice! this throws everything off just a little so in these instances you need to make sure not to let it add that extra 1.

### slimming these down

now that we have these 4 cases, we can start merging some of them.
the first merge i'd like to cover is `<0` and `>100`.

in the case of `<0`, we're currently doing a negation to bring it into the positive set, and that negation is missing for `>100`. this is basically the same as `abs(current_value + rotation) // 100` so we can swap them both out for this.
this does cause a small problem though - the `+ 1` on `<0`. however - not really. this is covered by our 4th case so by making this step always happen we can still run that 4th case after and it'll be dealt with.

now, always running it? what about the range `0 < x < 100`? all these numbers get 0s anyway so this is completely safe.

so now instead of 4 cases, we have 1 event that always happens and 1 conditional. much nicer to work with.

### final code

so now we can make a relatively simple reduce. the state variable will be shaped `(current_value, zeros)`.
we can now kind of view the reduce as 2 independant systems.

#### system 1: current_value

this is the simpler system, it's literally just tracking the current position on the dial. nothing fancy.

#### system 2: zeros

this is the fun part with the bulk of the logic. we're getting its old value, adding that `abs(state[0] + r) // 100` from earlier and then conditionally adding 1 if we didn't start on zero but are going below it.

```py
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
```
