import os


def data(fname):
    with open(fname, encoding="utf-8") as handle:
        return [int(line.strip()) for line in handle.readlines()]


def increased(measurements):
    return [
        pair[1]
        for pair in (zip(measurements[:-1], measurements[1:]))
        if pair[1] > pair[0]
    ]


def window(measurements):
    return [
        vals
        for vals in (
            zip(measurements[:-2], measurements[1:-1], measurements[2:] + [0, 0])
        )
    ]


test = data(os.path.join(os.path.dirname(__file__), "input/01.test"))
print(len(increased(test)))
print(len(increased([sum(vals) for vals in window(test)])))

real = data(os.path.join(os.path.dirname(__file__), "input/01.input"))
print(len(increased(real)))
print(len(increased([sum(vals) for vals in window(real)])))
