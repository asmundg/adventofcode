"""Day 04: Security Through Obscurity

Part 2 requires manual grepping to find the one human readable name,
but other than that, this is fairly mechanical. Heavy abuse of ordered
dict and sorting to get the frequency-then-alpha sorting right.

"""

from collections import OrderedDict
from textwrap import dedent
import os


def read_data() -> str:
    day = os.path.basename(__file__).split(".")[0].split("_")[1]
    fname = os.path.join(os.path.dirname(__file__), "input", f"{day}.input")

    with open(fname, encoding="utf-8") as handle:
        return handle.read().strip()


def parse(data: str):
    rooms = []
    for line in data.split("\n"):
        room, checksum = line[:-1].split("[")
        names, sector = room.rsplit("-", 1)
        rooms.append((names, int(sector), checksum))
    return rooms


def make_checksum(room):
    name, _sector, _checksum = room
    name = name.replace("-", "")

    # Count frequency by alphabetic order to ensure that things are
    # correctly ordered when we sort by frequency afterwards.
    chars = OrderedDict()
    for char in sorted(name):
        chars[char] = chars.get(char, 0) + 1

    return "".join(sorted(chars, key=lambda c: chars[c], reverse=True)[:5])


def decrypt(room):
    return "".join(
        [
            " " if c == "-" else chr((ord(c) - ord("a") + room[1]) % 26 + ord("a"))
            for c in room[0]
        ]
    )


def part1(rooms):
    valid = [room for room in rooms if make_checksum(room) == room[2]]
    return sum(room[1] for room in valid)


def part2(rooms):
    for room in rooms:
        if decrypt(room) == "northpole object storage":
            return room[1]


def test_part1():
    data = dedent(
        """
        aaaaa-bbb-z-y-x-123[abxyz]
        a-b-c-d-e-f-g-h-987[abcde]
        not-a-real-room-404[oarel]
        totally-real-room-200[decoy]
        """
    ).strip()
    assert part1(parse(data)) == 1514


def test_part2():
    assert decrypt(parse("qzmt-zixmtkozy-ivhz-343[]")[0]) == "very encrypted name"


if __name__ == "__main__":
    print(part1(parse(read_data())))
    print(part2(parse(read_data())))
