import os
from day_06 import read_data, solve, solve2


def test_part1():
    assert (
        solve(read_data(os.path.join(os.path.dirname(__file__), "input/06.test"))) == 42
    )


def test_part2():
    assert (
        solve2(
            read_data(os.path.join(os.path.dirname(__file__), "input/06-b.test")),
            ("SAN", "YOU"),
        )
        == 4
    )
