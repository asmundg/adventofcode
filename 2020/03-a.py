def tree(line, pos):
    pos %= (len(line) - 1)
    print(line, pos, line[pos] == "#")
    return line[pos] == "#"

with open("input/03.input") as f:
    res = [tree(line, y * 3) for y, line in enumerate(f.readlines())]
    print(sum(res))
