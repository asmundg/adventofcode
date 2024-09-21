"""Day 25: Let It Snow.

Well, that was a relief. Only complicated by the usual confusion about
which axis row# and col# refers to.
"""


def part1(target_x: int, target_y: int) -> int:
    coord = (1, 1)
    val = 20151125

    while coord != (target_x, target_y):
        val = val * 252533 % 33554393
        if coord[1] == 1:
            coord = (1, coord[0] + 1)
        else:
            coord = (coord[0] + 1, coord[1] - 1)

    return val


def test_part1():
    assert part1(6, 6) == 27995004


if __name__ == "__main__":
    print(part1(3019, 3010))
