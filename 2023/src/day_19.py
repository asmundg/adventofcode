"""Day 19: Aplenty

New record for ugly today. There is probably a nicer way of
structuring what is essentially an evaluation tree, but I couldn't
think of anything clever.

Part 2 requires tracking the ranges for each side of the eval tree and
just multiplying together the range sizes to get all possible
permutations.

"""

from dataclasses import dataclass
import functools
import os
import operator
import re
from textwrap import dedent

from typing import Dict, List, Tuple, TypeAlias


@dataclass
class Predicate:
    prop: str
    operator: str
    value: int
    target: str


Part: TypeAlias = Dict[str, int]
Rules: TypeAlias = Dict[str, List[Predicate]]


def read_data() -> str:
    day = os.path.basename(__file__).split(".")[0].split("_")[1]
    fname = os.path.join(os.path.dirname(__file__), "input", f"{day}.input")

    with open(fname, encoding="utf-8") as handle:
        return handle.read().strip()


def parse(data: str) -> Tuple[Rules, List[Part]]:
    rules: Rules = {}
    parts: List[Part] = []

    r, p = data.split("\n\n")
    for rule in r.split("\n"):
        m = re.match(r"([a-z]+){(.*)}", rule)
        assert m, ("Failed to parse", rule)
        label, logic = m.groups()
        for predicate in logic.split(","):
            if ":" in predicate:
                m = re.match(R"([a-z])([<>])([0-9]+):([a-zA-Z]+)", predicate)
                assert m, ("Failed to parse", predicate)
                prop, op, value, target = m.groups()
                rules.setdefault(label, []).append(
                    Predicate(prop, op, int(value), target)
                )
            else:
                rules.setdefault(label, []).append(Predicate("*", "*", 0, predicate))

    for part in p.split("\n"):
        m = re.match(r"{x=([0-9]+),m=([0-9]+),a=([0-9]+),s=([0-9]+)}", part)
        assert m, ("Failed to parse", part)
        parts.append({key: int(val) for key, val in zip("xmas", m.groups())})

    return rules, parts


def part1(data: str) -> int:
    rules, parts = parse(data)

    accepted = []
    for part in parts:
        rule = rules["in"]
        predicate_i = 0
        while predicate_i < len(rule):
            predicate = rule[predicate_i]
            if predicate.prop == "*":
                if predicate.target == "A":
                    accepted.append(part)
                    break
                if predicate.target == "R":
                    break
                rule = rules[predicate.target]
                predicate_i = 0
            else:
                op = operator.lt if predicate.operator == "<" else operator.gt
                if op(part[predicate.prop], predicate.value):
                    if predicate.target == "A":
                        accepted.append(part)
                        break
                    if predicate.target == "R":
                        break

                    rule = rules[predicate.target]
                    predicate_i = 0
                else:
                    predicate_i += 1

    return sum(sum(p.values()) for p in accepted)


def part2(data: str) -> int:
    rules, _ = parse(data)
    return count_valid(
        rules, "in", lo={key: 1 for key in "xmas"}, hi={key: 4000 for key in "xmas"}
    )


def count_valid(rules: Rules, rule_label: str, lo: Part, hi: Part) -> int:
    total = 0
    rule = rules[rule_label]
    for predicate in rule:
        if predicate.prop == "*":
            if predicate.target == "A":
                return total + functools.reduce(
                    operator.mul,
                    (h - (l - 1) for h, l in zip(hi.values(), lo.values())),
                )
            if predicate.target == "R":
                return total

            return total + count_valid(rules, predicate.target, lo, hi)

        if predicate.operator == "<":
            in_lo = lo
            in_hi = {
                key: min(val, predicate.value - 1) if key == predicate.prop else val
                for key, val in hi.items()
            }

            out_lo = {
                key: max(val, predicate.value) if key == predicate.prop else val
                for key, val in lo.items()
            }
            out_hi = hi

        if predicate.operator == ">":
            in_lo = {
                key: max(val, predicate.value + 1) if key == predicate.prop else val
                for key, val in lo.items()
            }
            in_hi = hi

            out_lo = lo
            out_hi = {
                key: min(val, predicate.value) if key == predicate.prop else val
                for key, val in hi.items()
            }

        if predicate.target == "A":
            total += functools.reduce(
                operator.mul,
                (h - (l - 1) for h, l in zip(in_hi.values(), in_lo.values())),
            )
        elif predicate.target == "R":
            pass
        else:
            total += count_valid(rules, predicate.target, in_lo, in_hi)
        lo, hi = out_lo, out_hi

    return total


def test_part1():
    data = dedent(
        """
        px{a<2006:qkq,m>2090:A,rfg}
        pv{a>1716:R,A}
        lnx{m>1548:A,A}
        rfg{s<537:gd,x>2440:R,A}
        qs{s>3448:A,lnx}
        qkq{x<1416:A,crn}
        crn{x>2662:A,R}
        in{s<1351:px,qqz}
        qqz{s>2770:qs,m<1801:hdj,R}
        gd{a>3333:R,R}
        hdj{m>838:A,pv}

        {x=787,m=2655,a=1222,s=2876}
        {x=1679,m=44,a=2067,s=496}
        {x=2036,m=264,a=79,s=2244}
        {x=2461,m=1339,a=466,s=291}
        {x=2127,m=1623,a=2188,s=1013}
        """
    ).strip()

    assert (part1(data)) == 19114


def test_part2():
    data = dedent(
        """
        px{a<2006:qkq,m>2090:A,rfg}
        pv{a>1716:R,A}
        lnx{m>1548:A,A}
        rfg{s<537:gd,x>2440:R,A}
        qs{s>3448:A,lnx}
        qkq{x<1416:A,crn}
        crn{x>2662:A,R}
        in{s<1351:px,qqz}
        qqz{s>2770:qs,m<1801:hdj,R}
        gd{a>3333:R,R}
        hdj{m>838:A,pv}

        {x=787,m=2655,a=1222,s=2876}
        {x=1679,m=44,a=2067,s=496}
        {x=2036,m=264,a=79,s=2244}
        {x=2461,m=1339,a=466,s=291}
        {x=2127,m=1623,a=2188,s=1013}
        """
    ).strip()

    assert (part2(data)) == 167409079868000


if __name__ == "__main__":
    print(part1(read_data()))
    print(part2(read_data()))
