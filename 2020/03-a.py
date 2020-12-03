def tree(line, pos):
    pos %= len(line) 
    print(line, pos, line[pos] == "#")
    return line[pos] == "#"

with open("input/03.input") as f:
    res = [tree(line.strip(), y * 3) for y, line in enumerate(f.readlines())]
    print(sum(res))
