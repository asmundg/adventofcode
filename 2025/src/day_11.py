"""Day 11: Reactor

DFS with a dynamic programming layer. Part 2 decomposes into counting
paths between the intermediary nodes. However, the data structure is
way more complex when starting from svr, so we need to cache the
subpath counts to avoid recomputing them (close to) infinite times.

"""

import functools
import os
from dataclasses import dataclass
from textwrap import dedent


@dataclass
class Problem:
    nodes: dict[str, tuple[str, ...]]


def read_data() -> str:
    day = os.path.basename(__file__).split(".")[0].split("_")[1]
    fname = os.path.join(os.path.dirname(__file__), "input", f"{day}.input")

    with open(fname, encoding="utf-8") as handle:
        return handle.read().strip()


def parse(data: str) -> Problem:
    p = Problem({})
    for line in data.split("\n"):
        labels = line.split()
        p.nodes[labels[0][:-1]] = tuple(labels[1:])
    return p


def find_paths(problem: Problem, start: str, end: str) -> int:
    @functools.cache
    def _find_paths(start: str, end: str) -> int:
        if start == end:
            return 1

        if start not in problem.nodes:
            return 0

        return sum(_find_paths(node, end) for node in problem.nodes[start])

    return _find_paths(start, end)


def part1(problem: Problem) -> int:
    return find_paths(problem, "you", "out")


def part2(problem: Problem) -> int:
    return (
        find_paths(problem, "svr", "fft") * find_paths(problem, "fft", "dac") * find_paths(problem, "dac", "out")
    ) + (find_paths(problem, "svr", "dac") * find_paths(problem, "dac", "fft") * find_paths(problem, "fft", "out"))


def test_part1() -> None:
    data = dedent(
        """
        aaa: you hhh
        you: bbb ccc
        bbb: ddd eee
        ccc: ddd eee fff
        ddd: ggg
        eee: out
        fff: out
        ggg: out
        hhh: ccc fff iii
        iii: out
        """
    ).strip()
    assert part1(parse(data)) == 5


def test_part2() -> None:
    data = dedent(
        """
        svr: aaa bbb
        aaa: fft
        fft: ccc
        bbb: tty
        tty: ccc
        ccc: ddd eee
        ddd: hub
        hub: fff
        eee: dac
        dac: fff
        fff: ggg hhh
        ggg: out
        hhh: out
        """
    ).strip()
    assert part2(parse(data)) == 2


if __name__ == "__main__":
    print(part1(parse(read_data())))
    print(part2(parse(read_data())))
