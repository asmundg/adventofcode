import os


def solve(x, y):
    dy = abs(y[0]) - 1
    pos = 0
    while dy > 0:
        pos, dy = pos + dy, dy - 1
        if dy == 0:
            print(pos)


def solve2(x, y):
    max_y = abs(y[0]) - 1
    min_y = y[0]
    max_x = x[1]

    hits = [
        (try_x, try_y)
        for try_x in range(max_x + 1)
        for try_y in range(min_y, max_y + 1)
        if hit(try_x, try_y, x, y)
    ]
    print(len(hits))


def hit(dx, dy, target_x, target_y):
    x, y, = (
        0,
        0,
    )

    while True:
        x, dx = x + dx, dx - 1 if dx > 0 else 0
        y, dy = y + dy, dy - 1

        if x > target_x[1] or y < target_y[0]:
            return False

        if x >= target_x[0] and y <= target_y[1]:
            return True


solve((20, 30), (-10, -5))
solve((209, 238), (-86, -59))

solve2((20, 30), (-10, -5))
solve2((209, 238), (-86, -59))
