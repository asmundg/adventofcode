import copy
import pprint


def line_of_sight(seats, coord):
    y, x = coord
    neighbours = [
        # up
        next(
            (
                seats[y_compare][x]
                for y_compare in reversed(range(0, y))
                if seats[y_compare][x] in ("#", "L")
            ),
            ".",
        ),
        # up/right
        next(
            (
                seats[y_compare][x_compare]
                for (y_compare, x_compare) in zip(
                    reversed(range(0, y)), range(x + 1, len(seats[y]))
                )
                if seats[y_compare][x_compare] in ("#", "L")
            ),
            ".",
        ),
        # right
        next(
            (
                seats[y][x_compare]
                for x_compare in range(x + 1, len(seats[y]))
                if seats[y][x_compare] in ("#", "L")
            ),
            ".",
        ),
        # down/right
        next(
            (
                seats[y_compare][x_compare]
                for (y_compare, x_compare) in zip(
                    range(y + 1, len(seats)), range(x + 1, len(seats[y]))
                )
                if seats[y_compare][x_compare] in ("#", "L")
            ),
            ".",
        ),
        # down
        next(
            (
                seats[y_compare][x]
                for y_compare in range(y + 1, len(seats))
                if seats[y_compare][x] in ("#", "L")
            ),
            ".",
        ),
        # down/left
        next(
            (
                seats[y_compare][x_compare]
                for (y_compare, x_compare) in zip(
                    range(y + 1, len(seats)), reversed(range(0, x))
                )
                if seats[y_compare][x_compare] in ("#", "L")
            ),
            ".",
        ),
        # left
        next(
            (
                seats[y][x_compare]
                for x_compare in reversed(range(0, x))
                if seats[y][x_compare] in ("#", "L")
            ),
            ".",
        ),
        # up/left
        next(
            (
                seats[y_compare][x_compare]
                for (y_compare, x_compare) in zip(
                    reversed(range(0, y)), reversed(range(0, x))
                )
                if seats[y_compare][x_compare] in ("#", "L")
            ),
            ".",
        ),
    ]
    return sum(neighbour == "#" for neighbour in neighbours)


def update(new, coord, old):
    occupied = line_of_sight(old, coord)

    y, x = coord
    if old[y][x] == "#" and occupied >= 5:
        new[y][x] = "L"
    elif old[y][x] == "L" and occupied == 0:
        new[y][x] = "#"
    else:
        new[y][x] = old[y][x]

    return new


def data():
    seats = []
    with open("input/11.input") as f:
        for line in f.readlines():
            seats.append([char for char in line.strip()])

    return seats


def main():
    seats = data()
    while True:
        old_seats = copy.deepcopy(seats)
        for y in range(len(seats)):
            for x in range(len(seats[y])):
                update(seats, (y, x), old_seats)

        # pprint.pprint(seats)
        print("*******")

        if old_seats == seats:
            print(len([seat for row in seats for seat in row if seat == "#"]))
            break


main()
