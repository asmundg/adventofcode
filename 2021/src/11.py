import os


def read_data(fname):
    with open(fname, encoding="utf-8") as handle:
        return [[int(num) for num in line.strip()] for line in handle.readlines()]


def neighbours(origin, height, width):
    x, y = origin
    max_x, max_y = height - 1, width - 1
    coords = []
    if x > 0:
        coords.append((x - 1, y))
    if x > 0 and y > 0:
        coords.append((x - 1, y - 1))
    if y > 0:
        coords.append((x, y - 1))
    if x < max_x and y > 0:
        coords.append((x + 1, y - 1))
    if x < max_x:
        coords.append((x + 1, y))
    if x < max_x and y < max_y:
        coords.append((x + 1, y + 1))
    if y < max_y:
        coords.append((x, y + 1))
    if x > 0 and y < max_y:
        coords.append((x - 1, y + 1))

    return coords


def solve(data, iterations=100):
    flashes = 0
    for _ in range(100):
        flashes += iterate(data)
    print(flashes)


def solve2(data):
    step = 0
    while True:
        step += 1
        if iterate(data) == len(data) * len(data[0]):
            print(step)
            break


def iterate(grid):
    height, width = len(grid), len(grid[0])
    for y in range(height):
        for x in range(width):
            grid[y][x] += 1

    while True:
        new = 0
        for y in range(height):
            for x in range(width):
                if grid[y][x] > 9:
                    grid[y][x] = 0
                    new += 1
                    for neighbour in neighbours((x, y), height, width):
                        if grid[neighbour[1]][neighbour[0]] > 0:
                            grid[neighbour[1]][neighbour[0]] += 1
        if new == 0:
            break

    flashes = 0
    for y in range(height):
        for x in range(width):
            if grid[y][x] == 0:
                flashes += 1

    return flashes


solve(read_data(os.path.join(os.path.dirname(__file__), "input/11.test")))
solve(read_data(os.path.join(os.path.dirname(__file__), "input/11.input")))

solve2(read_data(os.path.join(os.path.dirname(__file__), "input/11.test")))
solve2(read_data(os.path.join(os.path.dirname(__file__), "input/11.input")))
