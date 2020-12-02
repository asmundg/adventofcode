import re

r = re.compile("(\d+)-(\d+) ([a-z]): (.*)")

def check(line):
    one, two, char, pw = r.search(line).groups()
    num = len([c for c in pw if c == char])
    return (pw[int(one) - 1] == char) != (pw[int(two) - 1] == char)

with open("input/02.input") as f:
    res = [check(line) for line in f.readlines()]
    print(sum(res))
