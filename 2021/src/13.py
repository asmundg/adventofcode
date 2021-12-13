import re
import os


def read_data(fname):
    with open(fname, encoding="utf-8") as handle:
        coords = []
        while True:
            line = handle.readline().strip()
            if not line:
                break
            coords.append(tuple(int(num) for num in line.split(",")))

        return (
            set(coords),
            [
                (a, int(num))
                for a, num in [
                    re.match(".*([xy])=(\d+)", line.strip()).groups()
                    for line in handle.readlines()
                ]
            ],
        )


def fold_once(coords, fold_axis, fold_line):
    fold_axis = 0 if fold_axis == "x" else 1
    return {
        (
            coord[0] if fold_axis == 1 else fold_line - (coord[fold_axis] - fold_line),
            coord[1] if fold_axis == 0 else fold_line - (coord[fold_axis] - fold_line),
        )
        if coord[fold_axis] > fold_line
        else coord
        for coord in coords
    }


def solve(data):
    fold_axis, fold_line = data[1][0]
    print(len(fold_once(data[0], fold_axis, fold_line)))


def solve2(data):
    coords = data[0]

    for fold in data[1]:
        fold_axis, fold_line = fold
        coords = fold_once(coords, fold_axis, fold_line)

    for y in range(6):
        print("".join(["#" if (x, y) in coords else "." for x in range(39)]))


solve(read_data(os.path.join(os.path.dirname(__file__), "input/13.test")))
solve(read_data(os.path.join(os.path.dirname(__file__), "input/13.input")))

solve2(read_data(os.path.join(os.path.dirname(__file__), "input/13.test")))
solve2(read_data(os.path.join(os.path.dirname(__file__), "input/13.input")))
