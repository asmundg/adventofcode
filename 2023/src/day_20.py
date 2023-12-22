"""Day 20: Pulse Propagation

Well, that got interesting.

Part 1 is just implementing the algoritm as defined.

Part 2 isn't a general solution. I used graphviz to identify the
critical NAND gates. The target module is driven by a single NAND,
which is driven by four other NANDs. The penultimate NAND modules need
to all emit high at the same time to make the final NAND emit
low. This happens pretty rarely, as each penultimate module is driven
by a counter mechanism that only gets them into the right state every
few thousand buttons presses.

Since processing the circuit until we get the right output isn't
feasible, we instead identify the cycle time per penultimate
NAND. When we have this, LCM tells us the first time they all emit low
at the same time, producing the correct output.

"""

import functools
import os
from textwrap import dedent


def read_data() -> str:
    day = os.path.basename(__file__).split(".")[0].split("_")[1]
    fname = os.path.join(os.path.dirname(__file__), "input", f"{day}.input")

    with open(fname, encoding="utf-8") as handle:
        return handle.read().strip()


def parse(data: str):
    connections = {}
    types = {}

    for line in data.split("\n"):
        _source, _targets = line.split(" -> ")
        source = _source[1:] if _source != "broadcaster" else _source
        targets = _targets.split(", ")
        connections[source] = targets
        types[source] = _source[0]

    debug = []
    for conn in connections.values():
        for c in conn:
            if c not in connections:
                debug.append(c)

    for module in debug:
        connections[module] = []
        types[module] = "debug"

    state = {}
    for source, dests in connections.items():
        if types[source] == "%":
            state[source] = False
        for dest in dests:
            if types[dest] == "&":
                s = state.get(dest, {})
                s[source] = False
                state[dest] = s

    return connections, types, state


def part1(data: str) -> int:
    connections, types, state = parse(data)

    hi = 0
    lo = 0
    for _ in range(1000):
        pulses = [("broadcaster", False, "button")]
        while pulses:
            module, pulse, sender = pulses.pop(0)
            if pulse:
                hi += 1
            else:
                lo += 1

            if types[module] == "b":
                for m in connections[module]:
                    pulses.append((m, pulse, module))

            elif types[module] == "%":
                if not pulse:
                    state[module] = not state[module]
                    for m in connections[module]:
                        pulses.append((m, state[module], module))

            elif types[module] == "&":
                state[module][sender] = pulse
                for m in connections[module]:
                    pulses.append((m, not all(state[module].values()), module))

            elif types[module] == "debug":
                state[module] = pulse

    return hi * lo


def part2(data: str) -> int:
    connections, types, state = parse(data)

    # Derived from converting input to graphviz and just looking for
    # the penultimate nodes
    magic = {"mz", "jf", "bh", "sh"}
    n = 0
    cycles = {}
    while True:
        n += 1
        pulses = [("broadcaster", False, "button")]
        while pulses:
            module, pulse, sender = pulses.pop(0)

            if types[module] == "b":
                for m in connections[module]:
                    pulses.append((m, pulse, module))

            elif types[module] == "%":
                if not pulse:
                    state[module] = not state[module]
                    for m in connections[module]:
                        pulses.append((m, state[module], module))

            elif types[module] == "&":
                if (
                    module in magic
                    and all(state[module].values())
                    and not pulse
                    and module not in cycles
                ):
                    cycles[module] = n
                    if len(cycles) == len(magic):
                        return functools.reduce(lambda x, y: x * y, cycles.values())

                state[module][sender] = pulse
                for m in connections[module]:
                    pulses.append((m, not all(state[module].values()), module))


def test_part1_a():
    data = dedent(
        """
        broadcaster -> a, b, c
        %a -> b
        %b -> c
        %c -> inv
        &inv -> a
        """
    ).strip()

    assert part1(data) == 32000000


def test_part1_b():
    data = dedent(
        """
        broadcaster -> a
        %a -> inv, con
        &inv -> b
        %b -> con
        &con -> output
        """
    ).strip()

    assert part1(data) == 11687500


if __name__ == "__main__":
    print(part1(read_data()))
    print(part2(read_data()))
