"""Day 15: Warehouse Woes

Conceptually straight forward physics engine for implementing
Sokoban. Part 1 is linear and we just need to check that there's an
open space at the end of a sequence of boxes when pushing against one.

Part 2 gets into complex space, with boxes taking up more horizontal
space. I'm sure there are nicer way of modelling this, but I went with
one cell per coordinate to keep debugging simple. This means we need
to special case pushing in the various directions. Left/right is
essentially the same, but up/down can lead to one box pushing against
two boxes, recursively.

This means we need to keep track of which boxes we're pushing and
check if any of them push against any other boxes. If anything pushes
against a wall, we can't move. If not, we can move the boxes, but need
to move them starting at the ones furthest away to avoid overwrites.

It's not pretty, but it works.
"""

import os
from dataclasses import dataclass
from textwrap import dedent

from common import cartesian
from common.cartesian import Coord


@dataclass(frozen=True)
class World:
    start: Coord
    objects: dict[Coord, str]
    moves: list[Coord]


def read_data() -> str:
    day = os.path.basename(__file__).split(".")[0].split("_")[1]
    fname = os.path.join(os.path.dirname(__file__), "input", f"{day}.input")

    with open(fname, encoding="utf-8") as handle:
        return handle.read().strip()


def parse(data: str, wide: bool = False) -> World:
    objects: dict[Coord, str] = {}
    moves: list[Coord] = []
    start: Coord = (0, 0)

    map_lines, move_lines = data.split("\n\n")
    for y, line in enumerate(map_lines.split("\n")):
        for x, char in enumerate(line):
            if char == "#":
                if wide:
                    objects[(y, x * 2)] = "#"
                    objects[(y, x * 2 + 1)] = "#"
                else:
                    objects[(y, x)] = "#"
            elif char == "O":
                if wide:
                    objects[(y, x * 2)] = "["
                    objects[(y, x * 2 + 1)] = "]"
                else:
                    objects[(y, x)] = "O"
            elif char == "@":
                if wide:
                    objects[(y, x * 2)] = "@"
                    start = (y, x * 2)
                else:
                    objects[(y, x)] = "@"
                    start = (y, x)

    move_map = {"^": cartesian.UP, "v": cartesian.DOWN, "<": cartesian.LEFT, ">": cartesian.RIGHT}
    for move_line in move_lines.split("\n"):
        for char in move_line:
            moves.append(move_map[char])

    return World(start=start, objects=objects, moves=moves)


def debug(world: World) -> str:
    max_y = max(y for y, _ in world.objects)
    max_x = max(x for _, x in world.objects)
    return "\n".join("".join(world.objects.get((y, x), " ") for x in range(max_x + 1)) for y in range(max_y + 1))


def part1(world: World) -> int:
    robot = world.start
    for move in world.moves:
        candidate = cartesian.move(robot, move)
        if candidate not in world.objects:
            world.objects[candidate] = "@"
            world.objects.pop(robot)
            robot = candidate
        elif world.objects[candidate] == "O":
            update = candidate
            while True:
                update = cartesian.move(update, move)
                if update not in world.objects:
                    while update != robot:
                        previous = cartesian.move(update, cartesian.REVERSE[move])
                        world.objects[update] = world.objects[previous]
                        update = previous
                    world.objects.pop(update)
                    robot = candidate
                    break
                elif world.objects[update] == "O":
                    continue
                elif world.objects[update] == "#":
                    break
                else:
                    raise Exception("Oops")

    return sum(y * 100 + x for (y, x) in world.objects if world.objects[(y, x)] == "O")


def part2(world: World) -> int:
    robot = world.start
    for move in world.moves:
        candidate = cartesian.move(robot, move)
        if candidate not in world.objects:
            world.objects[candidate] = "@"
            world.objects.pop(robot)
            robot = candidate

        elif world.objects[candidate] in "[]":
            move_boxes: list[Coord] = [
                candidate if world.objects[candidate] == "[" else (candidate[0], candidate[1] - 1)
            ]
            check_boxes: list[Coord] = move_boxes[:]

            while check_boxes:
                check_box = check_boxes.pop()
                box_positions = (check_box, (check_box[0], check_box[1] + 1))
                if all(cartesian.move(c, move) not in world.objects for c in box_positions):
                    continue

                if any(world.objects.get(cartesian.move(c, move), "") == "#" for c in box_positions):
                    move_boxes = []
                    break

                if move == cartesian.LEFT:
                    if world.objects.get(cartesian.move(check_box, move), "") == "]":
                        check_boxes.append((check_box[0], check_box[1] - 2))
                        move_boxes.append(check_boxes[-1])

                elif move == cartesian.RIGHT:
                    if world.objects.get(cartesian.move((check_box[0], check_box[1] + 1), move), "") == "[":
                        check_boxes.append((check_box[0], check_box[1] + 2))
                        move_boxes.append(check_boxes[-1])
                else:
                    for part in box_positions:
                        to_check = cartesian.move(part, move)
                        if world.objects.get(to_check, "*") in "[]":
                            new_box = to_check if world.objects[to_check] == "[" else (to_check[0], to_check[1] - 1)
                            if new_box not in move_boxes:
                                check_boxes.append(new_box)
                                move_boxes.append(check_boxes[-1])

            if move_boxes:
                ordered = move_boxes
                if move == cartesian.UP:
                    ordered = sorted(move_boxes)
                elif move == cartesian.DOWN:
                    ordered = list(reversed(sorted(move_boxes)))
                elif move == cartesian.LEFT:
                    ordered = list(sorted(move_boxes, key=lambda coord: coord[1]))
                else:
                    ordered = list(reversed(sorted(move_boxes, key=lambda coord: coord[1])))

                for box in ordered:
                    target = cartesian.move(box, move)

                    world.objects[target] = "["
                    world.objects[(target[0], target[1] + 1)] = "]"
                    if move in (cartesian.RIGHT, cartesian.UP, cartesian.DOWN):
                        world.objects.pop(box)
                    if move in (cartesian.LEFT, cartesian.UP, cartesian.DOWN):
                        world.objects.pop((box[0], box[1] + 1))

                world.objects.pop(robot)
                robot = candidate
                world.objects[robot] = "@"

        elif world.objects[candidate] == "#":
            continue

        else:
            raise Exception("Oops")

    return sum(y * 100 + x for (y, x) in world.objects if world.objects[(y, x)] == "[")


def test_part1_small() -> None:
    data = dedent("""
    ########
    #..O.O.#
    ##@.O..#
    #...O..#
    #.#.O..#
    #...O..#
    #......#
    ########
    
    <^^>>>vv<v>>v<<
    """).strip()
    assert part1(parse(data)) == 2028


def test_part1() -> None:
    data = dedent("""
    ##########
    #..O..O.O#
    #......O.#
    #.OO..O.O#
    #..O@..O.#
    #O#..O...#
    #O..O..O.#
    #.OO.O.OO#
    #....O...#
    ##########
    
    <vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
    vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
    ><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
    <<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
    ^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
    ^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
    >^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
    <><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
    ^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
    v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^
    """).strip()
    assert part1(parse(data)) == 10092


def test_part2() -> None:
    data = dedent("""
    ##########
    #..O..O.O#
    #......O.#
    #.OO..O.O#
    #..O@..O.#
    #O#..O...#
    #O..O..O.#
    #.OO.O.OO#
    #....O...#
    ##########
    
    <vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
    vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
    ><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
    <<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
    ^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
    ^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
    >^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
    <><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
    ^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
    v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^
    """).strip()
    assert part2(parse(data, wide=True)) == 9021


if __name__ == "__main__":
    print(part1(parse(read_data())))
    print(part2(parse(read_data(), wide=True)))
