import os


def read_data(fname):
    with open(fname, encoding="utf-8") as handle:
        return parse(handle.readlines())


def parse(lines):
    return [line.strip() for line in lines]


def solve(data):
    pass


def test_something():
    assert False


if __name__ == "__main__":
    solve(read_data(os.path.join(os.path.dirname(__file__), "input/00.test")))
    solve(read_data(os.path.join(os.path.dirname(__file__), "input/00.input")))
