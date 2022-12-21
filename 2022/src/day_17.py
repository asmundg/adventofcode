"""Day 17: Pyroclastic Flow

Tetris! The part 1 implementation is quite simple, leveraging python's
set and comprehensions.

Part 2 is hairy and relies on heuristically detecting a cycle in the
moving parts. We're looking for points at which the jet position and
figure index are the same and spaced regularly both in number of
blocks and delta height. Once we've locked onto the cycle, we can
terminate once the remaining number of blocks is evenly divisible by
the number of blocks in the cycle.
"""

import itertools
import os
from typing import Dict, List, Set, TypeAlias, Tuple


def parse(fname: str) -> str:
    with open(fname, encoding="utf-8") as handle:
        return handle.read().strip()


# fmt: off
FIGURES = (
    set(((0, 0), (0, 1), (0, 2), (0, 3))),
    
    set(
        (        (2, 1),
         (1, 0), (1, 1), (1, 2),
                 (0, 1))),

    set((                (2, 2),
                         (1, 2),
         (0, 0), (0, 1), (0, 2))),

    set(((3, 0),
         (2, 0),
         (1, 0),
         (0, 0))),
    
    set(((1, 0), (1, 1),
         (0, 0), (0, 1))))
# fmt: on

Points: TypeAlias = Set[Tuple[int, int]]


def move(figure: Points, y: int, x: int) -> Points:
    return {(y + dy, x + dx) for dy, dx in figure}


def collides(stack: Points, figure: Points) -> bool:
    return (
        not all([p[0] > 0 for p in figure])
        or not all([0 <= p[1] <= 6 for p in figure])
        or len(stack & figure) > 0
    )


def print_stack(stack: Points, top: int) -> None:
    for y in range(top, 0, -1):
        print("".join(["#" if (y, x) in stack else "." for x in range(7)]))
    print()


def solve(fname: str, target: int) -> int:
    stack: Set[Tuple[int, int]] = set()
    figures = itertools.cycle(enumerate(FIGURES))
    jets = itertools.cycle(enumerate(parse(fname)))
    top = 0
    seen: Dict[Tuple[int, int], List[Tuple[int, int]]] = {}

    for block in range(target):
        figure_i, figure = next(figures)
        y = top + 4
        x = 2

        while True:
            jet_i, jet = next(jets)
            dx = -1 if jet == "<" else 1
            if not collides(stack, move(figure, y=y, x=x + dx)):
                x += dx
            if not collides(stack, move(figure, y=y - 1, x=x)):
                y -= 1
            else:
                moved = move(figure, y=y, x=x)
                top = max(top, *[c[0] for c in moved])
                stack.update(moved)

                if block > 0:
                    if (figure_i, jet_i) in seen:
                        seen[(figure_i, jet_i)].append((block, top))
                        check = [
                            (b[0] - a[0], b[1] - a[1])
                            for a, b in zip(
                                seen[(figure_i, jet_i)], seen[(figure_i, jet_i)][1:]
                            )
                        ]
                        # Steady cycle
                        if all(check[0] == c for c in check[-10:]):
                            # The remaining block count is evenly
                            # divisible by the block cycle length. We
                            # can terminate and multiply the top delta
                            # per cycle by the number of cycles left
                            # to the target.
                            if (target - block) % check[0][0] == 0:
                                return (
                                    top
                                    + check[0][1] * (target - block) // check[0][0]
                                    - 1
                                )
                    else:
                        seen[(figure_i, jet_i)] = [(block, top)]
                break
    return top


day = os.path.basename(__file__).split(".")[0].split("_")[1]
base = os.path.join(os.path.dirname(__file__), "input", f"{day}")

print(solve(f"{base}.test", 2022))
print(solve(f"{base}.input", 2022))

print(solve(f"{base}.test", 1000000000000))
print(solve(f"{base}.input", 1000000000000))
