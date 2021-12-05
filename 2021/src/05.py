import os


def read_data(fname):
    with open(fname, encoding="utf-8") as handle:
        return [
            [[int(num) for num in t.split(",")] for t in pair]
            for pair in [line.strip().split(" -> ") for line in handle.readlines()]
        ]


def solve(data, filter_diagonal=True):
    coords = {}
    for ((x1, y1), (x2, y2)) in data:
        if not filter_diagonal or x1 == x2 or y1 == y2:
            xstep = 1 if x2 > x1 else -1 if x2 < x1 else 0
            ystep = 1 if y2 > y1 else -1 if y2 < y1 else 0
            x = x1
            y = y1

            while x != x2 + xstep or y != y2 + ystep:
                coords[(x, y)] = coords.setdefault((x, y), 0) + 1
                x += xstep
                y += ystep

    return len([val for val in coords.values() if val > 1])


print(solve(read_data(os.path.join(os.path.dirname(__file__), "input/05.test"))))
print(solve(read_data(os.path.join(os.path.dirname(__file__), "input/05.input"))))

print(
    solve(
        read_data(os.path.join(os.path.dirname(__file__), "input/05.test")),
        filter_diagonal=False,
    ),
)
print(
    solve(
        read_data(os.path.join(os.path.dirname(__file__), "input/05.input")),
        filter_diagonal=False,
    )
)
