import functools
from dataclasses import dataclass, field
from typing import List
import re


def data():
    rules = []
    with open("input/19.input") as f:
        line = f.readline().strip()
        while line != "":
            rules.append(line)
            line = f.readline().strip()

        messages = [line.strip() for line in f.readlines()]
    return (rules, messages)


char_rule = re.compile(r'^(\d+): "(\w)"$')
other_rule = re.compile(r"^(\d+): (.*)$")


@dataclass
class Rule:
    char: str = ""
    sub_rules: List[List[str]] = field(default_factory=list)


def parse_rules(raw):
    rules = {}

    for line in raw:
        match = char_rule.match(line)
        if match:
            number, char = match.groups()
            rules[number] = Rule(char=char)
        else:
            number, rule = other_rule.match(line).groups()
            rules[number] = Rule(
                sub_rules=[group.split() for group in rule.split(" | ")]
            )
    return rules


def to_regex(rules, pos, cheat=False) -> str:
    rule = rules[pos]
    update = lambda acc, rule_id: acc + "(" + to_regex(rules, rule_id, cheat) + ")"

    # 0: 8 11
    # 8: 42 | 42 8 => 42+
    # 11: 42 31 | 42 11 31 => 42+31+ (note that there can't be more 31's than 42's)
    if cheat and pos in set(["8", "11"]):
        if pos == "8":
            return update("", "42") + "+"
        else:
            return "|".join(
                [
                    update("", "42") + f"{{{i}}}" + update("", "31") + f"{{{i}}}"
                    for i in range(1, 4)
                ]
            )
    else:
        return (
            rule.char
            if rule.char
            else "|".join(
                "(" + functools.reduce(update, group, "") + ")"
                for group in rule.sub_rules
            )
        )


def main():
    raw_rules, messages = data()
    parsed_rules = parse_rules(raw_rules)
    expr = "^" + to_regex(parsed_rules, "0") + "$"
    regex = re.compile(expr)
    part1 = [message for message in messages if regex.match(message)]

    expr = "^" + to_regex(parsed_rules, "0", cheat=True) + "$"
    regex = re.compile(expr)
    part2 = [message for message in messages if regex.match(message)]

    print(len(part1))
    print(len(part2))


main()
