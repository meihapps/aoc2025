# day 8: playground

this problem is about linking nodes together while minimising distance of links.

## formatting input

formatting is incredibly simple here, we just have new-line separated sets of comma-separated coordinates.

```py
def format_input(sample: bool = False):
    with open(f"{'sample_' if sample else ''}input.txt") as file:
        return [
            (int(x), int(y), int(z))
            for x, y, z in [i.split(",") for i in file.read().strip().split("\n")]
        ]
```

## both parts

for part 1, we're just doing the exact same thing as in part 2 but only doing the first 1000 connections and then stopping. this will form multiple smaller circuits that don't yet connect to one another.

one of the key components is getting all the circuits that contain a junction in our connection.

```py
def find_matching_circuits(circuit_sets: Circuits, cable: Cable) -> list[int]:
    return [
        index
        for index, circuit in enumerate(circuit_sets)
        if cable[0] in circuit or cable[1] in circuit
    ]
```

it's just a simple filter, nothing fancy.

another key component is getting all the connections so that we can sort them by distance.

```py
def get_n_cables(junctions: list[Junction], n: int | None = None):
    connections = sorted(
        [
            (node1, node2)
            for index1, node1 in enumerate(junctions)
            for index2, node2 in enumerate(junctions)
            if index1 < index2
        ],
        key=straight_line_distance,
    )
    return connections if n is None else connections[:n]
```

we're allowing only getting the first `n` so that we can use this for both parts.
this just goes over each node for each node, making sure to avoid duplicates with `index1 < index2`, sorting those tuples by distance.

and here's how we're sorting by distance:

```py
def straight_line_distance(
    cable: Cable,
) -> float:
    return dist(*cable)
```

this is just wrapping `math.dist` so that we can use it as a key. it just doesn't work well as a key otherwise.

when we go to add a new connection, we will have some cases to consider:
- this connection is between 2 entirely disconnected nodes, so it creates a new circuit
- this connection adds one node to a pre-existing circuit
- this connection connected 2 existing circuits together

first thing i'll cover is connecting two existing circuits together:

```py
def merge_circuits(
    circuit_sets: list[set[Junction]],
    matched_indices: list[int],
    edge: Cable,
) -> list[set[Junction]]:
    remaining = [
        circuit
        for idx, circuit in enumerate(circuit_sets)
        if idx not in matched_indices
    ]
    merged = set().union(
        *(circuit_sets[idx] for idx in matched_indices), {edge[0], edge[1]}
    )
    return remaining + [merged]
```

this makes one circuit that is the union of those two circuits, removes the existing circuits that just got merged and adds that one bigger circuit back.

the other two cases are, on their own, simpler so they weren't separated out into their own functions.

```py
def make_circuits(connections: Iterable[Cable]) -> Accumulator:
    return reduce(make_circuits_prime, connections, ([], None))

def make_circuits_prime(state: Accumulator, edge: Cable) -> Accumulator:
    circuit_sets, last_crossing_edge = state
    node_a, node_b = edge

    match find_matching_circuits(circuit_sets, edge):
        case []:
            return circuit_sets + [{node_a, node_b}], (node_a, node_b)

        case [primary_index]:
            circuit = circuit_sets[primary_index]
            updated_circuit = circuit | {node_a, node_b}
            crossing_edge = (
                edge
                if (node_a in circuit) ^ (node_b in circuit)
                else last_crossing_edge
            )

            return (
                circuit_sets[:primary_index]
                + [updated_circuit]
                + circuit_sets[primary_index + 1 :],
                crossing_edge,
            )

        case [_, *_] as matched_indices:
            return merge_circuits(
                circuit_sets, matched_indices, edge
            ), last_crossing_edge

        case _:
            assert False
```

in the instance of creating a new circuit, that's simply handled with `circuit_sets + [{node_a, node_b}]`

and in the instance of adding one node to an existing circuit, that's handled with `circuit_sets[:primary_index] + [updated_circuit] + circuit_sets[primary_index + 1 :]` with `updated_circuit` being `circuit_sets[primary_index] | {node_a, node_b}`

this all goes into a big unweildy match case that keeps track of the last edge to be added. there is a small logical error here where, in the instance of merging two circuits, the last edge added is reported incorrectly but this doesn't interfere with the end answer in this case so I haven't gotten around to fixing it yet.

## part 1

```py
def part_1() -> int:
    return reduce(
        lambda a, b: a * b,
        sorted(
            (len(i) for i in make_circuits(get_n_cables(format_input(), 1000))[0]),
            reverse=True,
        )[:3],
    )
```

we just take the first 1000 connections, making circuits of them, and then multiplying together the sizes of the 3 biggest circuits.

## part 2

```py
def part_2():
    _, last_cable = make_circuits(get_n_cables(format_input()))
    assert last_cable is not None
    return last_cable[0][0] * last_cable[1][0]
```

here we get all the cables, make a huge circuit of them and then multiply the x coordinates of the final cable for the output.
