import os


def data(fname):
    with open(fname, encoding="utf-8") as handle:
        return [line.strip() for line in handle.readlines()]


def parse(lines):
    res = []
    for line in lines:
        [cmd, num] = line.split()
        res.append([cmd, int(num)])
    return res


def move(steps):
    pos = {"pos": 0, "depth": 0}
    for [cmd, num] in steps:
        if cmd == "forward":
            pos["pos"] += num
        elif cmd == "down":
            pos["depth"] += num
        elif cmd == "up":
            pos["depth"] -= num
    return pos


def move_aim(steps):
    pos = {"pos": 0, "depth": 0, "aim": 0}
    for [cmd, num] in steps:
        if cmd == "forward":
            pos["pos"] += num
            pos["depth"] += num * pos["aim"]
        elif cmd == "down":
            pos["aim"] += num
        elif cmd == "up":
            pos["aim"] -= num
    return pos


test = data(os.path.join(os.path.dirname(__file__), "input/02.test"))
res = move(parse(test))
print(res, res["pos"] * res["depth"])
res2 = move_aim(parse(test))
print(res2, res2["pos"] * res2["depth"])

real = data(os.path.join(os.path.dirname(__file__), "input/02.input"))
res = move(parse(real))
print(res, res["pos"] * res["depth"])
res2 = move_aim(parse(real))
print(res2, res2["pos"] * res2["depth"])
