"""Day 17: Two Steps Forward

Ok, se we're traversing a maze, but available paths foward are
dependent on the path we took here. And the goal is shortest path to
the target. Sounds like breadth first to me.

"""

from hashlib import md5

from common.cartesian import DOWN, LEFT, RIGHT, UP, Coord, move


def part1(passcode: str) -> str:
    start = (0, 0)
    bounds = (3, 3)
    search = [(start, "")]

    while True:
        pos, path = search.pop(0)
        if pos == bounds:
            return path

        for path_suffix, direction, available in zip(
            "UDLR",
            (UP, DOWN, LEFT, RIGHT),
            [char in "bcdef" for char in md5((passcode + path).encode("ascii")).hexdigest()[:4]],
        ):
            candidate_pos = move(pos, direction)
            if available and 0 <= candidate_pos[0] <= bounds[0] and 0 <= candidate_pos[1] <= bounds[1]:
                search.append((candidate_pos, path + path_suffix))


def part2(passcode: str) -> int:
    start = (0, 0)
    bounds = (3, 3)
    search = [(start, "")]
    longest_path = 0

    while search:
        pos, path = search.pop(0)
        if pos == bounds:
            longest_path = max(len(path), longest_path)
            continue

        for path_suffix, direction, available in zip(
            "UDLR",
            (UP, DOWN, LEFT, RIGHT),
            [char in "bcdef" for char in md5((passcode + path).encode("ascii")).hexdigest()[:4]],
        ):
            candidate_pos = move(pos, direction)
            if available and 0 <= candidate_pos[0] <= bounds[0] and 0 <= candidate_pos[1] <= bounds[1]:
                search.append((candidate_pos, path + path_suffix))

    return longest_path


def test_part1() -> None:
    assert part1("ihgpwlah") == "DDRRRD"
    assert part1("kglvqrro") == "DDUDRLRRUDRD"
    assert part1("ulqzkmiv") == "DRURDRUDDLLDLUURRDULRLDUUDDDRR"


def test_part2() -> None:
    assert part2("ihgpwlah") == 370
    assert part2("kglvqrro") == 492
    assert part2("ulqzkmiv") == 830


if __name__ == "__main__":
    print(part1("awrkjxxr"))
    print(part2("awrkjxxr"))
