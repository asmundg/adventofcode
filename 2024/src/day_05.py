"""Day 5: Print Queue

I got into serious trouble here by trying to define a complete ordinal
rank for the rule set, before I realized that the rules have cyclic
dependencies and that they only work when we look at the subset that
is relevant for each set of pages.

Once we realize this, we can easily construct a sorted list by
inserting the next number where all numbers that come before it are
already in the list.
"""

import math
import os
from textwrap import dedent
from typing import TypeAlias

Rule: TypeAlias = list[int]
Pages: TypeAlias = list[int]


def read_data() -> str:
    day = os.path.basename(__file__).split(".")[0].split("_")[1]
    fname = os.path.join(os.path.dirname(__file__), "input", f"{day}.input")

    with open(fname, encoding="utf-8") as handle:
        return handle.read().strip()


def parse(data: str, use_p: bool = False) -> tuple[list[Rule], list[Pages]]:
    rule_lines, pages_lines = data.split("\n\n")

    rules: list[Rule] = [[int(n) for n in line.split("|")] for line in rule_lines.split("\n")]
    pages: list[Pages] = [[int(n) for n in line.split(",")] for line in pages_lines.split("\n")]

    return rules, pages


def sort(rules: list[Rule], values: list[int]) -> list[int]:
    after: dict[int, set[int]] = dict()
    for rule in rules:
        if rule[0] not in values or rule[1] not in values:
            continue

        if rule[0] not in after:
            after[rule[0]] = set()
        after[rule[0]].add(rule[1])

        if rule[1] not in after:
            after[rule[1]] = set()

    ordered: list[int] = []
    while after:
        for key in list(after.keys()):
            # If all numbers after us are already in the output, add
            # ourselves to the front.
            if all(val in ordered for val in after[key]):
                ordered.insert(0, key)
                after.pop(key)
                break

    return ordered


def part1(rules: list[Rule], page_sets: list[Pages]) -> int:
    sum = 0
    for pages in page_sets:
        if sort(rules, pages) == pages:
            sum += pages[math.floor(len(pages) / 2)]
    return sum


def part2(rules: list[Rule], page_sets: list[Pages]) -> int:
    sum = 0
    for pages in page_sets:
        if not sort(rules, pages) == pages:
            sum += sort(rules, pages)[math.floor(len(pages) / 2)]

    return sum


def test_part1() -> None:
    data = dedent("""
    47|53
    97|13
    97|61
    97|47
    75|29
    61|13
    75|53
    29|13
    97|29
    53|29
    61|53
    97|53
    61|29
    47|13
    75|47
    97|75
    47|61
    75|61
    47|29
    75|13
    53|13

    75,47,61,53,29
    97,61,53,29,13
    75,29,13
    75,97,47,61,53
    61,13,29
    97,13,75,29,47
    """).strip()
    assert part1(*parse(data)) == 143


def test_part2() -> None:
    data = dedent("""
    47|53
    97|13
    97|61
    97|47
    75|29
    61|13
    75|53
    29|13
    97|29
    53|29
    61|53
    97|53
    61|29
    47|13
    75|47
    97|75
    47|61
    75|61
    47|29
    75|13
    53|13

    75,47,61,53,29
    97,61,53,29,13
    75,29,13
    75,97,47,61,53
    61,13,29
    97,13,75,29,47
    """).strip()
    assert part2(*parse(data)) == 123


if __name__ == "__main__":
    print(part1(*parse(read_data())))
    print(part2(*parse(read_data())))
