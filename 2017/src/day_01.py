"""Day 01:"""

import os


def read_data() -> str:
    day = os.path.basename(__file__).split(".")[0].split("_")[1]
    fname = os.path.join(os.path.dirname(__file__), "input", f"{day}.input")

    with open(fname, encoding="utf-8") as handle:
        return handle.read().strip()


def parse(data: str) -> str:
    return data


def part1(captcha: str) -> int:
    total = 0
    for a, b in zip(captcha, captcha[1:] + captcha[0]):
        if a == b:
            total += int(a)
    return total


def part2(captcha: str) -> int:
    total = 0
    for i, char in enumerate(captcha):
        if char == captcha[(i + len(captcha) // 2) % len(captcha)]:
            total += int(char)
    return total


def test_part1() -> None:
    assert part1("1122") == 3
    assert part1("1111") == 4
    assert part1("1234") == 0
    assert part1("91212129") == 9


def test_part2() -> None:
    assert part2("1212") == 6
    assert part2("1221") == 0
    assert part2("123425") == 4
    assert part2("123123") == 12
    assert part2("12131415") == 4


if __name__ == "__main__":
    print(part1(parse(read_data())))
    print(part2(parse(read_data())))
