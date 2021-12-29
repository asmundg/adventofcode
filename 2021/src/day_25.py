import copy
import os


def read_data(fname):
    with open(fname, encoding="utf-8") as handle:
        return parse(handle.readlines())


def parse(lines):
    return [list(line.strip()) for line in lines]


def solve(data):
    count = 0
    moves = 1
    while moves:
        data, moves = step(data)
        count += 1

    print(count)


def step(data):
    moves = 0
    herds = {">": (0, 1), "v": (1, 0)}
    for move_type, move_dir in herds.items():
        new_data = copy.deepcopy(data)
        for y, line in enumerate(data):
            for x, point in enumerate(line):
                if point != move_type:
                    continue

                new_y, new_x = (
                    (y + move_dir[0]) % len(data),
                    (x + move_dir[1]) % len(line),
                )
                if data[new_y][new_x] == ".":
                    moves += 1
                    new_data[new_y][new_x] = point
                    new_data[y][x] = "."

        data = new_data

    return new_data, moves


def test_something():
    assert False


if __name__ == "__main__":
    solve(read_data(os.path.join(os.path.dirname(__file__), "input/25.test")))
    solve(read_data(os.path.join(os.path.dirname(__file__), "input/25.input")))
