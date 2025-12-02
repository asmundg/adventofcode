"""Day 02: Gift Shop

Chunking == string slicing. As usual, remembering how indices work for
range and slice is hard when I'm not fully awake. Could also have been
a regex.

"""

import os
from textwrap import dedent


def read_data() -> str:
    day = os.path.basename(__file__).split(".")[0].split("_")[1]
    fname = os.path.join(os.path.dirname(__file__), "input", f"{day}.input")

    with open(fname, encoding="utf-8") as handle:
        return handle.read().strip()


def parse(data: str) -> list[tuple[int, int]]:
    pairs: list[tuple[int, int]] = []
    for pair in data.split(","):
        a, b = pair.split("-")
        pairs.append((int(a), int(b)))
    return pairs


def part1_and_2(pairs: list[tuple[int, int]], all_ranges=False) -> int:
    total = 0
    for a, b in pairs:
        for n in range(a, b + 1):
            s = str(n)
            # All possible group lengths
            for seq in range(1, len(s) // 2 + 1) if all_ranges else ([len(s) // 2] if len(s) % 2 == 0 else []):
                # Check that it divides evenly
                if len(s) % seq == 0:
                    # Chunk
                    parts = [s[i : i + seq] for i in range(0, len(s), seq)]
                    if all(p == parts[0] for p in parts):
                        total += n
                        break
    return total


def test_part1() -> None:
    data = dedent(
        """
        11-22,95-115,998-1012,1188511880-1188511890,222220-222224,
1698522-1698528,446443-446449,38593856-38593862,565653-565659,
824824821-824824827,2121212118-2121212124
        """
    ).strip()
    assert part1_and_2(parse(data)) == 1227775554


def test_part2() -> None:
    data = dedent(
        """
        11-22,95-115,998-1012,1188511880-1188511890,222220-222224,
1698522-1698528,446443-446449,38593856-38593862,565653-565659,
824824821-824824827,2121212118-2121212124
        """
    ).strip()
    assert part1_and_2(parse(data), all_ranges=True) == 4174379265


if __name__ == "__main__":
    print(part1_and_2(parse(read_data())))
    print(part1_and_2(parse(read_data()), all_ranges=True))
