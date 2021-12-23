from day_23 import available_moves


def test_available_moves_0():
    assert sorted(
        available_moves(
            (6, 1),
            {
                (2, 1): "B",
                (2, 2): "A",
                (4, 1): "C",
                (4, 2): "D",
                (6, 1): "B",
                (6, 2): "C",
                (8, 1): "D",
                (8, 2): "A",
            },
        )
    ) == [
        (0, 0),
        (1, 0),
        (3, 0),
        (5, 0),
        (7, 0),
        (9, 0),
        (10, 0),
    ]


def test_available_moves_1():
    assert (
        available_moves(
            (4, 1),
            {
                (2, 1): "B",
                (2, 2): "A",
                (4, 1): "C",
                (4, 2): "D",
                (3, 0): "B",
                (6, 2): "C",
                (8, 1): "D",
                (8, 2): "A",
            },
        )
        == [(6, 1)]
    )


def test_available_moves_2():
    assert (
        available_moves(
            (4, 2),
            {
                (2, 1): "B",
                (2, 2): "A",
                (6, 1): "C",
                (4, 2): "D",
                (3, 0): "B",
                (6, 2): "C",
                (8, 1): "D",
                (8, 2): "A",
            },
        )
        == [(5, 0), (7, 0), (9, 0), (10, 0)]
    )


def test_available_moves_3():
    assert (
        available_moves(
            (3, 0),
            {
                (2, 1): "B",
                (2, 2): "A",
                (6, 1): "C",
                (5, 1): "D",
                (3, 0): "B",
                (6, 2): "C",
                (8, 1): "D",
                (8, 2): "A",
            },
        )
        == [(4, 2)]
    )


def test_available_moves_4():
    assert (
        available_moves(
            (2, 1),
            {
                (2, 1): "B",
                (2, 2): "A",
                (4, 2): "B",
                (5, 0): "D",
                (6, 1): "C",
                (6, 2): "C",
                (8, 1): "D",
                (8, 2): "A",
            },
        )
        == [(4, 1)]
    )


def test_available_moves_5():
    assert (
        available_moves(
            (8, 1),
            {
                (2, 2): "A",
                (4, 1): "B",
                (4, 2): "B",
                (5, 0): "D",
                (6, 1): "C",
                (6, 2): "C",
                (8, 1): "D",
                (8, 2): "A",
            },
        )
        == [(7, 0), (9, 0), (10, 0)]
    )


def test_available_moves_6():
    assert (
        available_moves(
            (8, 2),
            {
                (2, 2): "A",
                (4, 1): "B",
                (4, 2): "B",
                (5, 0): "D",
                (6, 1): "C",
                (6, 2): "C",
                (7, 0): "D",
                (8, 2): "A",
            },
        )
        == [(9, 0), (10, 0)]
    )


def test_available_moves_7():
    assert (
        available_moves(
            (7, 0),
            {
                (2, 2): "A",
                (4, 1): "B",
                (4, 2): "B",
                (5, 0): "D",
                (6, 1): "C",
                (6, 2): "C",
                (7, 0): "D",
                (9, 1): "A",
            },
        )
        == [(8, 2)]
    )


def test_available_moves_8():
    assert (
        available_moves(
            (5, 0),
            {
                (2, 2): "A",
                (4, 1): "B",
                (4, 2): "B",
                (5, 0): "D",
                (6, 1): "C",
                (6, 2): "C",
                (8, 2): "D",
                (9, 0): "A",
            },
        )
        == [(8, 1)]
    )


def test_available_moves_9():
    assert (
        available_moves(
            (9, 0),
            {
                (2, 2): "A",
                (4, 1): "B",
                (4, 2): "B",
                (6, 1): "C",
                (6, 2): "C",
                (8, 1): "D",
                (8, 2): "D",
                (9, 0): "A",
            },
        )
        == [(2, 1)]
    )


def test_available_moves_10():
    assert (
        available_moves(
            (9, 0),
            {
                (2, 2): "B",
                (4, 1): "A",
                (4, 2): "B",
                (6, 1): "C",
                (6, 2): "C",
                (8, 1): "D",
                (8, 2): "D",
                (9, 0): "A",
            },
        )
        == []
    )
