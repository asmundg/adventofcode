"""Day 3: 
"""

import os


def parse(fname: str) -> str:
    with open(fname, encoding="utf-8") as handle:
        return handle.read().strip()


DIRECTIONS = {"^": (-1, 0), ">": (0, 1), "v": (1, 0), "<": (0, -1)}


def solve(directions: str, num_santas: int = 1) -> int:
    pos = [(0, 0)] * num_santas
    visited = set(pos)
    for i, char in enumerate(directions):
        direction = DIRECTIONS[char]
        santa = i % num_santas
        pos[santa] = (pos[santa][0] + direction[0], pos[santa][1] + direction[1])
        visited.add(pos[santa])
    return len(visited)


day = os.path.basename(__file__).split(".")[0].split("_")[1]
base = os.path.join(os.path.dirname(__file__), "input", f"{day}")
assert solve(">") == 2
assert solve("^>v<") == 4
assert solve("^v^v^v^v^v") == 2
print(solve(parse(f"{base}.input")))

assert solve("^v", 2) == 3
assert solve("^>v<", 2) == 3
assert solve("^v^v^v^v^v", 2) == 11
print(solve(parse(f"{base}.input"), 2))
