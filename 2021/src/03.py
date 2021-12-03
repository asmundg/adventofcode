import os


def data(fname):
    with open(fname, encoding="utf-8") as handle:
        return [line.strip() for line in handle.readlines()]


def col_sum(lines, index):
    return sum([1 for line in lines if line[index] == "1"])


def gamma(lines):
    res = ""
    for index in range(len(lines[0])):
        res += "1" if col_sum(lines, index) > len(lines) / 2 else "0"
    return int(res, 2)


def epsilon(lines):
    res = ""
    for index in range(len(lines[0])):
        res += "0" if col_sum(lines, index) > len(lines) / 2 else "1"
    return int(res, 2)


def oxygen(lines):
    index = 0
    prefix = ""
    filtered = lines[:]
    while len(filtered) > 1:
        prefix += "1" if col_sum(filtered, index) >= len(filtered) / 2 else "0"
        filtered = [line for line in filtered if line.startswith(prefix)]
        index += 1
    return int(filtered[0], 2)


def co2(lines):
    index = 0
    prefix = ""
    filtered = lines[:]
    while len(filtered) > 1:
        prefix += "0" if col_sum(filtered, index) >= len(filtered) / 2 else "1"
        filtered = [line for line in filtered if line.startswith(prefix)]
        index += 1
    return int(filtered[0], 2)


d = data(os.path.join(os.path.dirname(__file__), "input/03.test"))
print(gamma(d), epsilon(d), gamma(d) * epsilon(d), oxygen(d) * co2(d))


d = data(os.path.join(os.path.dirname(__file__), "input/03.input"))
print(gamma(d), epsilon(d), gamma(d) * epsilon(d), oxygen(d) * co2(d))
