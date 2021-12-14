import os


def read_data(fname):
    with open(fname, encoding="utf-8") as handle:
        initial = handle.readline().strip()
        handle.readline().strip()
        return (
            initial,
            {
                key: val
                for key, val in [
                    line.strip().split(" -> ") for line in handle.readlines()
                ]
            },
        )


def solve(data, steps=10):
    seq = data[0]
    res = {}
    for i in range(len(seq) - 1):
        res = merge_dict(res, lookup(seq[i] + seq[i + 1], steps, data[1], {}))
    res[seq[-1]] = res.get(seq[-1], 0) + 1

    freq = sorted(res, key=lambda char: res[char])
    print(res[freq[-1]] - res[freq[0]])


def lookup(pair, step, insertions, cache):
    if step == 0:
        return {pair[0]: 1}

    if (pair, step) in cache:
        return cache[(pair, step)]

    insertion = insertions[pair[0] + pair[1]]
    val = merge_dict(
        lookup(pair[0] + insertion, step - 1, insertions, cache),
        lookup(insertion + pair[1], step - 1, insertions, cache),
    )
    cache[(pair, step)] = val
    return val


def merge_dict(a, b):
    d = {}
    d.update(a)
    for key in b:
        d[key] = a.get(key, 0) + b[key]
    return d


solve(read_data(os.path.join(os.path.dirname(__file__), "input/14.test")))
solve(read_data(os.path.join(os.path.dirname(__file__), "input/14.input")))

solve(read_data(os.path.join(os.path.dirname(__file__), "input/14.test")), steps=40)
solve(read_data(os.path.join(os.path.dirname(__file__), "input/14.input")), steps=40)
