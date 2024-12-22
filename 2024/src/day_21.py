"""Day 21: Keypad Conundrum

Oh boy, this was fun. Trying to mentally model chords producing each
other recursively was extremely taxing. Fortunately, we don't really
need to understand what's going on to solve this, other than to
realize that we only need to figure out which chords on the
directional keypad produces a given 'higher-level' chord.

The confusing part is that the number of steps needed will vary in
weird ways across the different layers. Meaning we need to compute all
potential paths between two locations, check which N-depth chord is
required to get there and then get the cheapest one for the given N.

The numeric keypad lookup table isn't strictly necessary, but it
provided a neat sanity check.

"""

import functools
import os
from itertools import permutations
from textwrap import dedent


def read_data() -> str:
    day = os.path.basename(__file__).split(".")[0].split("_")[1]
    fname = os.path.join(os.path.dirname(__file__), "input", f"{day}.input")

    with open(fname, encoding="utf-8") as handle:
        return handle.read().strip()


def parse(data: str) -> list[str]:
    return [line for line in data.split("\n")]


def find_keypad_sequence(code: str) -> list[str]:
    def p(s: str) -> set[str]:
        return {"".join(p) for p in permutations(s)}

    keypad = {
        "7": {
            "8": [">"],
            "9": [">>"],
            "4": ["v"],
            "5": p("v>"),
            "6": p("v>>"),
            "1": ["vv"],
            "2": p("vv>"),
            "3": p("vv>>"),
            "0": p("vvv>") - {"vvv>"},
            "A": p("vvv>>") - {"vvv>>"},
        },
        "8": {
            "7": ["<"],
            "9": [">"],
            "4": p("v<"),
            "5": ["v"],
            "6": p("v>"),
            "1": p("vv<"),
            "2": ["vv"],
            "3": p("vv>"),
            "0": ["vvv"],
            "A": p("vvv>"),
        },
        "9": {
            "7": ["<<"],
            "8": ["<"],
            "4": p("v<<"),
            "5": p("v<"),
            "6": ["v"],
            "1": p("vv<<"),
            "2": p("vv<"),
            "3": ["vv"],
            "0": p("vvv<"),
            "A": p("vvv"),
        },
        "4": {
            "7": ["^"],
            "8": p("^>"),
            "9": p("^>>"),
            "5": [">"],
            "6": [">>"],
            "1": ["v"],
            "2": p("v>"),
            "3": p("v>>"),
            "0": p("vv>") - {"vv>"},
            "A": p("vv>>") - {"vv>>"},
        },
        "5": {
            "7": p("^<"),
            "8": ["^"],
            "9": p("^>"),
            "4": ["<"],
            "6": [">"],
            "1": p("v<"),
            "2": ["v"],
            "3": p("v>"),
            "0": ["vv"],
            "A": p("vv>"),
        },
        "6": {
            "7": p("^<<"),
            "8": p("^<"),
            "9": ["^"],
            "4": p("<"),
            "5": ["<"],
            "1": p("v<<"),
            "2": p("v<"),
            "3": ["v"],
            "0": p("vv<"),
            "A": p("vv"),
        },
        "1": {
            "7": ["^^"],
            "8": p("^^>"),
            "9": p("^^>>"),
            "4": ["^"],
            "5": p("^>"),
            "6": p("^>>"),
            "2": [">"],
            "3": [">>"],
            "0": [">v"],
            "A": p("v>>") - {"v>>"},
        },
        "2": {
            "7": p("^^<"),
            "8": ["^^"],
            "9": p("^^>"),
            "4": p("^<"),
            "5": ["^"],
            "6": p("^>"),
            "1": ["<"],
            "3": p(">"),
            "0": ["v"],
            "A": p("v>"),
        },
        "3": {
            "7": p("^^<<"),
            "8": p("^^<"),
            "9": ["^^"],
            "4": p("^<<"),
            "5": p("^<"),
            "6": ["^"],
            "1": p("<<"),
            "2": ["<"],
            "0": p("v<"),
            "A": ["v"],
        },
        "0": {
            "7": p("^^^<") - {"<^^^"},
            "8": ["^^^"],
            "9": p("^^^>"),
            "4": p("^^<") - {"<^^"},
            "5": ["^^"],
            "6": p("^^>"),
            "1": p("^<") - {"<^"},
            "2": ["^"],
            "3": p("^>"),
            "A": [">"],
        },
        "A": {
            "7": p("^^^<<") - {"<<^^^"},
            "8": p("^^^<"),
            "9": ["^^^"],
            "4": p("^^<<") - {"<<^^"},
            "5": p("^^<"),
            "6": ["^^"],
            "1": p("^<<") - {"<<^"},
            "2": p("^<"),
            "3": ["^"],
            "0": ["<"],
        },
    }
    sequences = [""]
    for char, prev_char in zip(code, "A" + code):
        sequences = [seq + chord + "A" for chord in keypad[prev_char][char] for seq in sequences]

    return sequences


def find_direction_sequence(char: str, from_char: str) -> list[str]:
    keypad = {
        "^": {"^": [""], "A": [">"], "<": ["v<"], "v": ["v"], ">": ["v>", ">v"]},
        "A": {"^": ["<"], "A": [""], "<": ["v<<", "<v<"], "v": ["<v", "v<"], ">": ["v"]},
        "<": {"^": [">^"], "A": [">>^", ">^>"], "<": [""], "v": [">"], ">": [">>"]},
        "v": {"^": ["^"], "A": ["^>", ">^"], "<": ["<"], "v": [""], ">": [">"]},
        ">": {"^": ["^<", "<^"], "A": ["^"], "<": ["<<"], "v": ["<"], ">": [""]},
    }
    return [s + "A" for s in keypad[from_char][char]]


@functools.cache
def count_steps(chord: str, n: int) -> int:
    if n == 0:
        return len(chord)

    seq = 0
    for char, last_char in zip(chord, "A" + chord):
        char_chords = find_direction_sequence(char, last_char)
        seq += min(count_steps(char_chord, n - 1) for char_chord in char_chords)
    return seq


def part1(codes: list[str]) -> int:
    cost = 0
    for code in codes:
        cost += min(count_steps(seq, 2) for seq in find_keypad_sequence(code)) * int(code[:-1])
    return cost


def part2(codes: list[str]) -> int:
    cost = 0
    for code in codes:
        cost += min(count_steps(seq, 25) for seq in find_keypad_sequence(code)) * int(code[:-1])
    return cost


def test_part1() -> None:
    data = dedent("""
    029A
    980A
    179A
    456A
    379A
    """).strip()
    assert part1(parse(data)) == 126384


if __name__ == "__main__":
    print(part1(parse(read_data())))
    print(part2(parse(read_data())))
