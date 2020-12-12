from dataclasses import dataclass
import re


def data():
    data_re = re.compile(r"^(N|S||E|W|L|R|F)(\d+)$")
    with open("input/12.input") as f:
        return [data_re.match(line).groups() for line in f.readlines()]


orientation = ["N", "E", "S", "W"]


@dataclass
class State:
    y: int = 0
    x: int = 0
    heading: str = "E"


def move_direction(op, state, amount):
    if op == "N":
        state.y += amount
    elif op == "E":
        state.x += amount
    elif op == "S":
        state.y -= amount
    elif op == "W":
        state.x -= amount


def update(state, change):
    (op, amount) = change[0], int(change[1])
    if op == "L":
        state.heading = orientation[
            (orientation.index(state.heading) - (amount // 90)) % len(orientation)
        ]
    elif op == "R":
        state.heading = orientation[
            (orientation.index(state.heading) + (amount // 90)) % len(orientation)
        ]
    if op == "F":
        move_direction(state.heading, state, amount)
    else:
        move_direction(op, state, amount)

    print(op, state)


def main():
    state = State()
    [update(state, change) for change in data()]
    print(abs(state.x) + abs(state.y))


main()
