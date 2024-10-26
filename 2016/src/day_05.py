"""Day 05: How About a Nice Game of Chess?

MD5 again, which means Python's batteries included are super useful.

"""

import hashlib
import itertools
import os
from typing import Dict, Generator, Tuple


def read_data() -> str:
    day = os.path.basename(__file__).split(".")[0].split("_")[1]
    fname = os.path.join(os.path.dirname(__file__), "input", f"{day}.input")

    with open(fname, encoding="utf-8") as handle:
        return handle.read().strip()


def find_pw(door_id: str, prefix: int = 5) -> Generator[Tuple[str, str], None, None]:
    for i in itertools.count(start=0):
        h = hashlib.md5((door_id + str(i)).encode("ascii")).hexdigest()
        if h.startswith("0" * prefix):
            yield (h[5], h[6])


def part1(door_id: str) -> str:
    return "".join(t[0] for t in itertools.islice(find_pw(door_id), 8))


def part2(door_id: str) -> str:
    chars: Dict[str, str] = {}
    positions = "01234567"
    for pos, val in find_pw(door_id):
        if pos in positions and pos not in chars:
            chars[pos] = val
            if len(chars) == len(positions):
                break

    return "".join(chars[p] for p in positions)


def test_part1() -> None:
    assert part1("abc") == "18f47a30"


def test_part2() -> None:
    assert part2("abc") == "05ace8e3"


if __name__ == "__main__":
    print(part1(read_data()))
    print(part2(read_data()))
