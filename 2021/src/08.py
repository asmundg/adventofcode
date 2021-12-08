import os


def read_data(fname):
    with open(fname, encoding="utf-8") as handle:
        return [
            [part.split() for part in line.strip().split("|")]
            for line in handle.readlines()
        ]


def solve(data):
    known = {1: 2, 4: 4, 7: 3, 8: 7}
    print(sum([1 for line in data for num in line[1] if len(num) in known.values()]))


valid = [
    "abcefg",
    "cf",
    "acdeg",
    "acdfg",
    "bcdf",
    "abdfg",
    "abdefg",
    "acf",
    "abcdefg",
    "abcdfg",
]


def solve2(data):
    result = 0
    for (wires, display) in data:
        wiremap = search("", "abcdefg", wires)
        result += int(
            "".join([str(valid.index(map_wire(wiremap, number))) for number in display])
        )
    print(result)


def search(guess, candidates, controls):
    if not candidates:
        for control in controls:
            if map_wire(guess, control) not in valid:
                return

        return guess

    for wire in candidates:
        result = search(
            guess + wire, "".join([c for c in candidates if c != wire]), controls
        )
        if result:
            return result


def map_wire(wiremap, number):
    return "".join(sorted([wiremap[ord(c) - ord("a")] for c in number]))


solve(read_data(os.path.join(os.path.dirname(__file__), "input/08.test")))
solve(read_data(os.path.join(os.path.dirname(__file__), "input/08.input")))

solve2(read_data(os.path.join(os.path.dirname(__file__), "input/08.test")))
solve2(read_data(os.path.join(os.path.dirname(__file__), "input/08.input")))
