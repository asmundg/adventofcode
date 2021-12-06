import os


def read_data(fname):
    with open(fname, encoding="utf-8") as handle:
        return [line.strip() for line in handle.readlines()]


def solve(data):
    pass


solve(read_data(os.path.join(os.path.dirname(__file__), "input/00.test")))
solve(read_data(os.path.join(os.path.dirname(__file__), "input/00.input")))
