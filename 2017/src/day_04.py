"""Day 04: High-Entropy Passphrases

Short problem texts are often trouble, but in this case we just need
to count the occurrences of each thing. Which itertools can do for us.

For part 2, we sort the letters of each word and then do the check
from part 1.

"""

import itertools
import os


def read_data() -> str:
    day = os.path.basename(__file__).split(".")[0].split("_")[1]
    fname = os.path.join(os.path.dirname(__file__), "input", f"{day}.input")

    with open(fname, encoding="utf-8") as handle:
        return handle.read().strip()


def parse(data: str) -> list[list[str]]:
    lines: list[list[str]] = []
    for line in data.split("\n"):
        lines.append(line.split())
    return lines


def part1(candidates: list[list[str]]) -> int:
    valid = 0
    for candidate in candidates:
        for k, v in itertools.groupby(sorted(candidate)):
            if len(list(v)) > 1:
                break
        else:
            valid += 1
    return valid


def part2(candidates: list[list[str]]) -> int:
    return part1([[str(sorted(word)) for word in candidate] for candidate in candidates])


def test_part1() -> None:
    assert part1(parse("aa bb cc dd ee"))
    assert not part1(parse("aa bb cc dd aa"))
    assert part1(parse("aa bb cc dd aaa"))


def test_part2() -> None:
    assert part2(parse("abcde fghij"))
    assert not part2(parse("abcde xyz ecdab"))
    assert part2(parse("a ab abc abd abf abj"))
    assert part2(parse("iiii oiii ooii oooi oooo"))
    assert not part2(parse("oiii ioii iioi iiio"))


if __name__ == "__main__":
    print(part1(parse(read_data())))
    print(part2(parse(read_data())))
