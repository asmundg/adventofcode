import functools

rows = 127
columns = 7


def bisect(range, char, lower):
    mid = sum(range) / 2
    print(range, char, mid)
    if lower:
        return (range[0], mid)
    else:
        return (mid + 1, range[1])


def seatId(p):
    print("***")
    row = functools.reduce(
        lambda row, char: bisect(row, char, char == "F"), p[0:7], (0, rows)
    )
    column = functools.reduce(
        lambda column, char: bisect(column, char, char == "L"), p[7:10], (0, columns)
    )
    print(row[0], column[0])
    return row[0] * 8 + column[0]


with open("input/05.input") as f:
    passes = [seatId(p) for p in f.readlines()]
    print(passes)
    print(max(passes))
