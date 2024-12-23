"""Day 23: LAN Party

I love the included batteries in Python. Today, we'll use `set` to
track sets of connected computers.

We can build sets of connected nodes by first creating an initial map
of connections for each node, build a set of networks that initially
contain each single node, and then for each set, iterate over each
node and add the node to the set if the connected set is a subset of
the node's connections.

This gives us a set of all networks and we can simply find the largest
one.

"""

import os
from textwrap import dedent


def read_data() -> str:
    day = os.path.basename(__file__).split(".")[0].split("_")[1]
    fname = os.path.join(os.path.dirname(__file__), "input", f"{day}.input")

    with open(fname, encoding="utf-8") as handle:
        return handle.read().strip()


def parse(data: str) -> dict[str, set[str]]:
    connections: dict[str, set[str]] = dict()
    for line in data.split("\n"):
        a, b = line.split("-")
        if a not in connections:
            connections[a] = set()
        if b not in connections:
            connections[b] = set()
        connections[a].add(b)
        connections[b].add(a)
    return connections


def part1(connections: dict[str, set[str]]) -> int:
    sets: set[tuple[str, ...]] = set()

    for node, neighbors in connections.items():
        if node[0] != "t":
            continue
        for neighbor in neighbors:
            target = {node, neighbor}
            for other_node, other_neighbors in connections.items():
                if target.issubset(other_neighbors):
                    sets.add(tuple(sorted([node, neighbor, other_node])))

    return len(sets)


def part2(connections: dict[str, set[str]]) -> str:
    sets: set[tuple[str, ...]] = set([(k,) for k in connections])

    while True:
        found = False
        next_sets = set()
        for connected in sets:
            search = set(connected)
            for node, neighbors in connections.items():
                if search.issubset(neighbors):
                    next_sets.add(tuple(sorted(connected + (node,))))
                    found = True
        if not found:
            break
        else:
            sets = next_sets

    return ",".join(sorted(sets, key=lambda x: len(x))[-1])


def test_part1() -> None:
    data = dedent("""
    kh-tc
    qp-kh
    de-cg
    ka-co
    yn-aq
    qp-ub
    cg-tb
    vc-aq
    tb-ka
    wh-tc
    yn-cg
    kh-ub
    ta-co
    de-co
    tc-td
    tb-wq
    wh-td
    ta-ka
    td-qp
    aq-cg
    wq-ub
    ub-vc
    de-ta
    wq-aq
    wq-vc
    wh-yn
    ka-de
    kh-ta
    co-tc
    wh-qp
    tb-vc
    td-yn
    """).strip()
    assert part1(parse(data)) == 7


def test_par2() -> None:
    data = dedent("""
    kh-tc
    qp-kh
    de-cg
    ka-co
    yn-aq
    qp-ub
    cg-tb
    vc-aq
    tb-ka
    wh-tc
    yn-cg
    kh-ub
    ta-co
    de-co
    tc-td
    tb-wq
    wh-td
    ta-ka
    td-qp
    aq-cg
    wq-ub
    ub-vc
    de-ta
    wq-aq
    wq-vc
    wh-yn
    ka-de
    kh-ta
    co-tc
    wh-qp
    tb-vc
    td-yn
    """).strip()
    assert part2(parse(data)) == "co,de,ka,ta"


if __name__ == "__main__":
    print(part1(parse(read_data())))
    print(part2(parse(read_data())))
