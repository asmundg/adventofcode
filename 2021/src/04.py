import os


def data(fname):
    with open(fname, encoding="utf-8") as handle:
        numbers = [int(num) for num in next(handle).split(",")]
        boards = []
        next(handle)
        while True:
            boards.append(
                [[int(num) for num in next(handle).strip().split()] for _ in range(5)]
            )
            try:
                next(handle)
            except StopIteration:
                return (numbers, boards)


def columns(board):
    return [[board[row][col] for row in range(5)] for col in range(5)]


def game(numbers, boards):
    for num in numbers:
        for board in boards:
            for row in board:
                for pos in range(len(row)):
                    if row[pos] == num:
                        row[pos] = None

                        if len([el for el in row if el is None]) == 5:
                            return num, board

                        for column in columns(board):
                            if len([el for el in column if el is None]) == 5:
                                return num, board


def solve(path):
    numbers, boards = data(path)
    num, board = game(numbers, boards)
    print(
        num,
        sum(val for row in board for val in row if val is not None),
        sum(val for row in board for val in row if val is not None) * num,
    )


def solve2(path):
    numbers, boards = data(path)
    while True:
        num, winner = game(numbers, boards)
        if len(boards) == 1:
            break

        boards = [board for board in boards if board is not winner]

    print(
        num,
        sum(val for row in boards[0] for val in row if val is not None),
        sum(val for row in boards[0] for val in row if val is not None) * num,
    )


solve(os.path.join(os.path.dirname(__file__), "input/04.test"))
solve(os.path.join(os.path.dirname(__file__), "input/04.input"))

solve2(os.path.join(os.path.dirname(__file__), "input/04.test"))
solve2(os.path.join(os.path.dirname(__file__), "input/04.input"))
