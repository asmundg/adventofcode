import re

r = re.compile("(\d+)-(\d+) ([a-z]): (.*)")

def check(line):
    min, max, char, pw = r.search(line).groups()
    num = len([c for c in pw if c == char])
    return num >= int(min) and num <= int(max)

with open("input/02.input") as f:
    res = [check(line) for line in f.readlines()]
    print(sum(res))
