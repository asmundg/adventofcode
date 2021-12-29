"""Universal Orbit Map

Double-linked graphs! The lookaside means we can start from either end
without additional data structures.
"""
import os


def read_data(fname):
    with open(fname, encoding="utf-8") as handle:
        return parse(handle.readlines())


def parse(lines):
    com = {}
    orbits = {}
    for a, b in [line.strip().split(")") for line in lines]:
        orbits.setdefault(a, {"parent": None, "children": []})["children"].append(b)
        orbits.setdefault(b, {"parent": a, "children": []})["parent"] = a
    return orbits


def solve(orbits):
    total = 0
    search = [("COM", 0)]

    while search:
        root, depth = search.pop()
        total += depth

        for node in orbits[root]["children"]:
            search.append((node, depth + 1))

    return total


def solve2(orbits, search):
    paths = []
    for target in search:
        node = orbits[target]
        path = []
        while node["parent"] is not None:
            node = orbits[node["parent"]]
            path.insert(0, node)
        paths.append(path)

    n = 0
    while paths[0][n] == paths[1][n]:
        n += 1
    return len(paths[0]) - n + len(paths[1]) - n


if __name__ == "__main__":
    print(solve(read_data(os.path.join(os.path.dirname(__file__), "input/06.input"))))
    print(
        solve2(
            read_data(os.path.join(os.path.dirname(__file__), "input/06.input")),
            ("SAN", "YOU"),
        )
    )
