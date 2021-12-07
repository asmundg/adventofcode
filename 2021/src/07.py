import os


def read_data(fname):
    with open(fname, encoding="utf-8") as handle:
        return sorted(
            [int(num) for line in handle.readlines() for num in line.strip().split(",")]
        )


def solve(data):
    best = (0, None)
    for pos in range(data[0], data[-1] + 1):
        cost = sum([abs(num - pos) for num in data])
        if best[1] is None or cost < best[1]:
            best = (pos, cost)
    print(best)


def solve2(data):
    fac = {}
    for n in range(data[-1] + 1):
        fac[n] = 0 if n == 0 else fac[n - 1] + n

    best = (0, None)
    for pos in range(data[0], data[-1] + 1):
        cost = sum([fac[abs(num - pos)] for num in data])
        if best[1] is None or cost < best[1]:
            best = (pos, cost)
    print(best)


solve(read_data(os.path.join(os.path.dirname(__file__), "input/07.test")))
solve(read_data(os.path.join(os.path.dirname(__file__), "input/07.input")))

solve2(read_data(os.path.join(os.path.dirname(__file__), "input/07.test")))
solve2(read_data(os.path.join(os.path.dirname(__file__), "input/07.input")))
