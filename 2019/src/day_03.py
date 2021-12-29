import os


def read_data(fname):
    with open(fname, encoding="utf-8") as handle:
        return parse(handle.readlines())


def parse(lines):
    parsed = []
    for line in lines:
        segments = []
        x, y, total_steps = 0, 0, 0
        for segment in line.split(","):
            direction, steps = segment[0], int(segment[1:])
            total_steps += steps
            if direction == "R":
                segments.append(((x, y), (x + steps, y), total_steps))
                x += steps
            elif segment[0] == "L":
                segments.append(((x, y), (x - steps, y), total_steps))
                x -= steps
            elif segment[0] == "U":
                segments.append(((x, y), (x, y + steps), total_steps))
                y += steps
            elif segment[0] == "D":
                segments.append(((x, y), (x, y - steps), total_steps))
                y -= steps
        parsed.append(segments)
    return parsed


def solve(data):
    lowest_distance = 10 ** 10
    lowest_steps = 10 ** 10

    for (a_x0, a_y0), (a_x1, a_y1), a_steps in data[0]:
        for (b_x0, b_y0), (b_x1, b_y1), b_steps in data[1]:
            # horizontal a, vertical b
            if (
                a_x0 != a_x1
                and b_x0 == b_x1
                and min(a_x0, a_x1) < b_x0 < max(a_x0, a_x1)
                and min(b_y0, b_y1) < a_y0 < max(b_y0, b_y1)
            ):
                distance = abs(b_x0) + abs(a_y0)
                steps = a_steps - abs(a_x1 - b_x0) + b_steps - abs(b_y1 - a_y0)
            # vertical a, horizontal b
            elif (
                a_y0 != a_y1
                and b_y0 == b_y1
                and min(a_y0, a_y1) < b_y0 < max(a_y0, a_y1)
                and min(b_x0, b_x1) < a_x0 < max(b_x0, b_x1)
            ):
                distance = abs(b_y0) + abs(a_x0)
                steps = a_steps - abs(a_y1 - b_y0) + b_steps - (abs(b_x1 - a_x0))
            else:
                continue

            if distance < lowest_distance:
                lowest_distance = distance
            if steps < lowest_steps:
                lowest_steps = steps

    return lowest_distance, lowest_steps


if __name__ == "__main__":
    print(solve(read_data(os.path.join(os.path.dirname(__file__), "input/03.input"))))
