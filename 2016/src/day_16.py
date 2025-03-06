"""Day 16: Dragon Checksum

Straight forward mechanical manipulation of data. Once again, I
suspected part 2 would scale out of control and once again, it's
perfectly possible to compute naively.

"""


def generate_data(length: int, data: str) -> str:
    while len(data) < length:
        data = data + "0" + "".join("1" if c == "0" else "0" for c in reversed(data))
    return data[:length]


def checksum(data: str) -> str:
    checksum = data
    while True:
        checksum = "".join("1" if a == b else "0" for a, b in zip(checksum[0::2], checksum[1::2]))
        if len(checksum) % 2:
            return checksum


def part1(length: int, initial: str) -> str:
    return checksum(generate_data(length, initial))


def test_checksum() -> None:
    assert checksum("110010110100") == "100"


def test_part1() -> None:
    assert part1(20, "10000") == "01100"


if __name__ == "__main__":
    print(part1(272, "10111100110001111"))
    print(part1(35651584, "10111100110001111"))
