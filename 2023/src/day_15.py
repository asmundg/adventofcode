"""Day 15: Lens Library

Completely mechanical task today, but requires some careful
reading. Which is not easy that early in the morning. Took me a while
to realize that labels and box ids are not the same thing.
"""

import os

from typing import List, TypeAlias, Tuple

Data: TypeAlias = List[str]


def read_data() -> str:
    day = os.path.basename(__file__).split(".")[0].split("_")[1]
    fname = os.path.join(os.path.dirname(__file__), "input", f"{day}.input")

    with open(fname, encoding="utf-8") as handle:
        return handle.read().strip()


def parse(data: str) -> Data:
    return data.split(",")


def hash(data: str) -> int:
    val = 0
    for char in data:
        val += ord(char)
        val *= 17
        val %= 256
    return val


def part1(data: str) -> int:
    parts = parse(data)
    return sum(hash(part) for part in parts)


def part2(data: str) -> int:
    parts = parse(data)
    boxes: List[List[Tuple[str, int]]] = [[] for _ in range(256)]
    for part in parts:
        if part[-1] == "-":
            label = part[:-1]
            box_id = hash(label)
            boxes[box_id] = [lens for lens in boxes[box_id] if lens[0] != label]
        else:
            label = part.split("=")[0]
            f = int(part.split("=")[1])
            box_id = hash(label)
            if any(lens for lens in boxes[box_id] if lens[0] == label):
                boxes[box_id] = [
                    (lens[0], f) if lens[0] == label else (lens[0], lens[1])
                    for lens in boxes[box_id]
                ]
            else:
                boxes[box_id].append((label, f))

    total = 0
    for box_id, box in enumerate(boxes, start=1):
        total += sum((box_id) * i * lens[1] for i, lens in enumerate(box, start=1))
    return total


def test_part1():
    assert part1("HASH") == 52
    assert (part1("rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7")) == 1320


def test_part2():
    assert (part2("rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7")) == 145


if __name__ == "__main__":
    print(part1(read_data()))
    print(part2(read_data()))
