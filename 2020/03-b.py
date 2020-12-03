def tree(line, pos):
    pos %= (len(line) - 1)
    print(line, pos, line[pos] == "#")
    return line[pos] == "#"

with open("input/03.input") as f:
    lines = f.readlines()
    trees = [sum([tree(line, y * xd) for y, line in enumerate(lines)]) for xd in [1, 3, 5, 7]]
    final = sum([tree(line, y / 2) for y, line in enumerate(lines) if y % 2 == 0])
    print(trees, final)
    print(reduce(lambda x, y: x * y, trees) * final)
