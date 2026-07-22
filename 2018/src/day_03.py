"""Day 03:"""

import os
from dataclasses import dataclass

@dataclass
class Square:
    id: int
    top: int
    left: int
    height: int
    width: int

def read_data() -> str:
    day = os.path.basename(__file__).split(".")[0].split("_")[1]
    fname = os.path.join(os.path.dirname(__file__), "input", f"{day}.input")

    with open(fname, encoding="utf-8") as handle:
        return handle.read().strip()

def parse(data: str) -> list[Square]:
    squares = []
    for line in data.split("\n"):
        claim_id, _, coord, ext = line.split(" ")
        left, top = coord.split(",")
        width, height = ext.split("x")
        squares.append(Square(id=int(claim_id[1:]), top=int(top[:-1]), left=int(left), width=int(width), height=int(height)))
    return squares

def coords(sq: Square) -> set[tuple[int,int]]:
    coords: set[tuple[int,int]] = set()
    for y in range(sq.height):
        for x in range(sq.width):
            coords.add((sq.top + y, sq.left + x))
    return coords
            
    
def part1(data: list[Square]) -> int:
    seen: set[tuple[int,int]] = set()
    overlap: set[tuple[int,int]] = set()
    for claim in data:
        c = coords(claim)
        overlap.update(seen.intersection(c))
        seen.update(c)

    return len(overlap)

def part2(data: list[Square]) -> int:
    for claim in data:
        for other_claim in data:
            if claim is other_claim:
                continue
            if coords(other_claim).intersection(coords(claim)):
                break
        else:
            return claim.id

    raise Exception("no solution")

if __name__ == "__main__":
    print(part1(parse(read_data())))
    print(part2(parse(read_data())))
