import os


def read_data(fname):
    with open(fname, encoding="utf-8") as handle:
        return [
            int(num) for line in handle.readlines() for num in line.strip().split(",")
        ]


def to_lifecycle(data):
    lifecycle = [0 for _ in range(9)]
    for num in data:
        lifecycle[num] += 1
    return lifecycle


def solve(data, gens=80):
    lifecycle = to_lifecycle(data)
    for _ in range(gens):
        next_gen = lifecycle[0]
        for gen in range(8):
            lifecycle[gen] = lifecycle[gen + 1]
        lifecycle[6] += next_gen
        lifecycle[8] = next_gen
    print(sum(lifecycle))


solve(read_data(os.path.join(os.path.dirname(__file__), "input/06.test")))
solve(read_data(os.path.join(os.path.dirname(__file__), "input/06.input")))

solve(read_data(os.path.join(os.path.dirname(__file__), "input/06.test")), gens=256)
solve(read_data(os.path.join(os.path.dirname(__file__), "input/06.input")), gens=256)
