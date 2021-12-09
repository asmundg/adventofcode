import functools
import os


def read_data(fname):
    with open(fname, encoding="utf-8") as handle:
        return [[int(num) for num in line.strip()] for line in handle.readlines()]


def neighbours(origin, data):
    max_x, max_y = len(data[0]) - 1, len(data) - 1
    x, y = origin
    coords = []
    if x > 0:
        coords.append((x - 1, y))
    if x < max_x:
        coords.append((x + 1, y))
    if y > 0:
        coords.append((x, y - 1))
    if y < max_y:
        coords.append((x, y + 1))
    return coords


def lowest_points(data):
    points = []
    for y in range(len(data)):
        for x in range(len(data[y])):
            point = data[y][x]
            neighbour_coordinates = neighbours((x, y), data)
            higher = [
                coord
                for coord in neighbour_coordinates
                if data[coord[1]][coord[0]] > point
            ]

            if len(higher) == len(neighbour_coordinates):
                points.append((x, y))

    return points


def solve(data):
    points = lowest_points(data)
    print(sum([data[point[1]][point[0]] + 1 for point in points]))


def solve2(data):
    points = lowest_points(data)
    basins = []
    import copy

    for point in points:
        d = copy.deepcopy(data)
        d[point[1]][point[0]] = 99
        walk([point], d)
        basins.append(sum([1 for line in d for point in line if point == 99]))
    print(
        functools.reduce(
            lambda acc, cur: acc * cur, sorted(basins, reverse=True)[:3], 1
        )
    )


def walk(points, data):
    if not points:
        return

    next_points = [
        coord
        for point in points
        for coord in neighbours(point, data)
        if data[coord[1]][coord[0]] < 9
    ]
    for point in next_points:
        data[point[1]][point[0]] = 99

    walk(next_points, data)


solve(read_data(os.path.join(os.path.dirname(__file__), "input/09.test")))
solve(read_data(os.path.join(os.path.dirname(__file__), "input/09.input")))

solve2(read_data(os.path.join(os.path.dirname(__file__), "input/09.test")))
solve2(read_data(os.path.join(os.path.dirname(__file__), "input/09.input")))
