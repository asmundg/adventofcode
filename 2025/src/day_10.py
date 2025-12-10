"""Day 10: Factory

This sneakily starts out looking like a BFS, but is actually linear equations! Equations means z3-solver."""

import os
from dataclasses import dataclass
from textwrap import dedent

import z3


@dataclass
class Problem:
    target: str
    buttons: list[set[int]]
    joltage: tuple[int, ...]


def read_data() -> str:
    day = os.path.basename(__file__).split(".")[0].split("_")[1]
    fname = os.path.join(os.path.dirname(__file__), "input", f"{day}.input")

    with open(fname, encoding="utf-8") as handle:
        return handle.read().strip()


def parse(data: str) -> list[Problem]:
    problems: list[Problem] = []
    for line in data.split("\n"):
        parts = line.split()
        target = parts[0][1:-1]
        buttons = [set([int(n) for n in button[1:-1].split(",")]) for button in parts[1:-1]]
        joltage = tuple(int(n) for n in parts[-1][1:-1].split(","))
        problems.append(Problem(target, buttons, joltage))
    return problems


def part1(problems: list[Problem]) -> int:
    return sum(min_walk(problem.target, problem.buttons) for problem in problems)


def flip(state: str, button: set[int]) -> str:
    res = ""
    for i, c in enumerate(state):
        if i in button:
            res += "#" if c == "." else "."
        else:
            res += c
    return res


def min_walk(target: str, buttons: list[set[int]]) -> int:
    init_state = "".join("." for _ in target)
    search = [(flip(init_state, button), 1) for button in buttons]
    best = {"".join("." for _ in target): 0}

    while search:
        state, steps = search.pop(0)
        if steps >= best.get(state, float("inf")):
            continue
        else:
            best[state] = steps

        if state == target:
            continue

        for button in buttons:
            new_state = flip(state, button)
            search.append((new_state, steps + 1))

    return best[target]


def part2(problems: list[Problem]) -> int:
    total = 0
    for problem in problems:
        button_presses = [z3.Int(str(n)) for n in range(len(problem.buttons))]
        solver = z3.Optimize()
        for press in button_presses:
            solver.add(press >= 0)
        for i, target in enumerate(problem.joltage):
            solver.add(sum(press for press, button in zip(button_presses, problem.buttons) if i in button) == target)
        solver.minimize(sum(button_presses))
        assert solver.check() == z3.sat
        model = solver.model()
        total += sum(model[n].as_long() if model[n] is not None else 0 for n in button_presses)

    return total


def test_part1() -> None:
    data = dedent(
        """
        [.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
        [...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
        [.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}
        """
    ).strip()
    assert part1(parse(data)) == 7


def test_part2() -> None:
    data = dedent(
        """
        [.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
        [...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
        [.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}
        """
    ).strip()
    assert part2(parse(data)) == 33


if __name__ == "__main__":
    print(part1(parse(read_data())))
    print(part2(parse(read_data())))
