import heapq
import os

# A* Time!


def read_data(fname):
    with open(fname, encoding="utf-8") as handle:
        return [[int(num) for num in line.strip()] for line in handle.readlines()]


# We could probably do something better here for more speed.
def null_h(_):
    return 0


def solve(data):
    start = (0, 0)
    max_y, max_x = len(data) - 1, len(data[0]) - 1
    goal = (max_y, max_x)

    def lookup(coord):
        return data[coord[0]][coord[1]]

    path = astar(start, goal, null_h, lookup, max_y, max_x)
    print(sum([data[coord[0]][coord[1]] for coord in path[1:]]))


def solve2(data):
    start = (0, 0)
    max_y, max_x = (len(data) * 5 - 1, len(data[0]) * 5 - 1)
    goal = (max_y, max_x)

    def lookup(coord):
        data_y, data_x = coord[0] % len(data), coord[1] % len(data[0])
        offset = coord[0] // len(data) + coord[1] // len(data[0])
        corrected = (data[data_y][data_x] + offset) % 10 + (
            1 if data[data_y][data_x] + offset > 9 else 0
        )
        return corrected

    path = astar(start, goal, null_h, lookup, max_y, max_x)
    print(
        sum([lookup(coord) for coord in path[1:]]),
    )


def neighbors(origin, max_y, max_x):
    y, x = origin
    coords = []
    if x > 0:
        coords.append((y, x - 1))
    if x < max_x:
        coords.append((y, x + 1))
    if y > 0:
        coords.append((y - 1, x))
    if y < max_y:
        coords.append((y + 1, x))
    return coords


def reconstruct_path(came_from, current):
    total_path = [current]
    while current in came_from:
        current = came_from[current]
        total_path.insert(0, current)
    return total_path


def astar(start, goal, h, data_lookup, max_y, max_x):
    # Yay, wikipedia!
    open_set = [(0, start)]
    came_from = {}
    g_score = {start: 0}
    f_score = {start: h(start)}

    while open_set:
        current = heapq.heappop(open_set)[1]
        if current == goal:
            return reconstruct_path(came_from, current)

        for neighbor in neighbors(current, max_y, max_x):
            tentative_g_score = g_score[current] + data_lookup(neighbor)
            if tentative_g_score < g_score.get(neighbor, 999999999):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + h(neighbor)

                if neighbor not in open_set:
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))


solve(read_data(os.path.join(os.path.dirname(__file__), "input/15.test")))
solve(read_data(os.path.join(os.path.dirname(__file__), "input/15.input")))

solve2(read_data(os.path.join(os.path.dirname(__file__), "input/15.test")))
solve2(read_data(os.path.join(os.path.dirname(__file__), "input/15.input")))
