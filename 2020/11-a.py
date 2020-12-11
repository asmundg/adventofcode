import pprint
import functools

seats = {}

with open("input/11.input") as f:
    for y, row in enumerate(f.readlines()):
        for x, char in enumerate(row.strip()):
            print(y, x, char)
            seats[(y, x)] = char


def update(new, coord, old):
    occupied = 0
    for y in range(coord[0] - 1, coord[0] + 2):
        for x in range(coord[1] - 1, coord[1] + 2):
            if old.get((y, x), ".") == "#":
                occupied += 1

    if old[coord] == "#" and occupied >= 5:
        new[coord] = "L"
    elif old[coord] == "L" and occupied == 0:
        new[coord] = "#"
    else:
        new[coord] = old[coord]

    return new


while True:
    old_seats = seats
    seats = functools.reduce(lambda acc, cur: update(acc, cur, seats), seats, {})

    pprint.pprint(seats)
    print("*******")

    if old_seats == seats:
        print(len([coord for coord in seats if seats[coord] == "#"]))
        break
