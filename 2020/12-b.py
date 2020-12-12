from dataclasses import dataclass
import re


def data():
    data_re = re.compile(r"^(N|S||E|W|L|R|F)(\d+)$")
    with open("input/12.input") as f:
        return [data_re.match(line).groups() for line in f.readlines()]


@dataclass
class State:
    y: int = 0
    x: int = 0
    wp_rel_x: int = 10
    wp_rel_y: int = 1


def update(state, change):
    (op, amount) = change[0], int(change[1])
    if op == "N":
        state.wp_rel_y += amount
    elif op == "E":
        state.wp_rel_x += amount
    elif op == "S":
        state.wp_rel_y -= amount
    elif op == "W":
        state.wp_rel_x -= amount
    elif op == "F":
        state.x += state.wp_rel_x * amount
        state.y += state.wp_rel_y * amount
    elif op == "L":
        for _ in range(amount // 90):
            wp_rel_x = state.wp_rel_x
            wp_rel_y = state.wp_rel_y
            state.wp_rel_y = wp_rel_x
            state.wp_rel_x = -wp_rel_y
    elif op == "R":
        for _ in range(amount // 90):
            wp_rel_x = state.wp_rel_x
            wp_rel_y = state.wp_rel_y
            state.wp_rel_y = -wp_rel_x
            state.wp_rel_x = wp_rel_y

    print(op, amount, state)


def main():
    state = State()
    [update(state, change) for change in data()]
    print(abs(state.x) + abs(state.y))


main()
