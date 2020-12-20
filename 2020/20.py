import functools
import numpy
import math
import re
import copy
from typing import List, Set


class Tile:
    def __init__(self, id, data):
        self.id = id

        self.layouts = [Layout(self, data, i) for i in range(8)]

    def __hash__(self):
        return hash(self.id)


class Layout:
    def __init__(self, tile: Tile, data, layout: int):
        self.tile = tile
        self.layout = layout
        self.data = numpy.rot90(numpy.flip(data, 0) if layout > 4 else data, layout % 4)
        self.top = self.data[0, :]
        self.right = self.data[:, -1]
        self.bottom = self.data[-1, :]
        self.left = self.data[:, 0]


def data():
    tile_re = re.compile(r"^Tile (\d+):$")
    tiles = set()
    with open("input/20.input") as f:
        while True:
            tile_id = tile_re.match(f.readline().strip()).group(1)
            data = numpy.array([[c for c in f.readline().strip()] for _ in range(10)])
            tiles.add(Tile(tile_id, data))
            if not f.readline():
                break

    return tiles


def fits(layouts: List[Layout], layout: Layout, sides):
    if len(layouts) == 0:
        return True

    if len(layouts) < sides:
        return (layouts[-1].right == layout.left).all()

    if len(layouts) % sides == 0:
        return (layouts[len(layouts) - sides].bottom == layout.top).all()

    return (layouts[len(layouts) - sides].bottom == layout.top).all() and (
        layouts[len(layouts) - 1].right == layout.left
    ).all()


tried = set()


def solve(tiles: Set[Tile], layouts: List[Layout], sides):
    prefix = "  " * len(layouts)

    print(prefix, len(tiles), [(layout.tile.id) for layout in layouts])

    if not tiles:
        return layouts

    remaining = tiles.copy()
    while remaining:
        tile = remaining.pop()

        key = ",".join(
            [
                layout.tile.id + "_" + str(layout.layout)
                for layout in layouts[len(layouts) - sides * 2 :]
            ]
            + [tile.id, "-"]
            + sorted(tile.id for tile in tiles)
        )
        if key in tried:
            continue

        for layout in tile.layouts:
            if fits(layouts, layout, sides):
                solution = solve(
                    set([t for t in tiles if t.id != tile.id]),
                    layouts + [layout],
                    sides,
                )
                if solution:
                    return solution
        else:
            tried.add(key)


def to_images(layouts):
    sides = int(math.sqrt(len(layouts)))
    data = [
        functools.reduce(
            lambda arr, i: numpy.delete(arr, 0 if i < 2 else -1, i % 2),
            range(4),
            layout.data,
        )
        for layout in layouts
    ]

    image = numpy.concatenate(
        [
            numpy.concatenate(data[col * sides : (col + 1) * sides], axis=1)
            for col in range(sides)
        ],
        axis=0,
    )

    return [
        numpy.rot90(numpy.flip(image, 0) if i >= 4 else image, i % 4) for i in range(8)
    ]


def monster_coordinates(origin_j, origin_i):
    # fmt: off
    monster = ["                  # ",
               "#    ##    ##    ###",
               " #  #  #  #  #  #   "]
    # fmt: on
    coordinates = [
        (origin_j + j, origin_i + i)
        for j, line in enumerate(monster)
        for i, char in enumerate(line)
        if char == "#"
    ]

    return coordinates


def find_monsters(image):
    image = copy.deepcopy(image)
    for j in range(len(image)):
        for i in range(len(image[j])):
            coordinates = monster_coordinates(j, i)
            # Check for monster locations out of bounds
            if [
                coord
                for coord in coordinates
                if (
                    coord[0] < 0
                    or coord[0] >= len(image)
                    or coord[1] < 0
                    or coord[1] >= len(image)
                )
            ]:
                continue

            # Check if all coordinates has an entry
            matches = [coord for coord in coordinates if image[coord] == "#"]

            # If so mark those locations, to help counting and avoid double matches
            if len(matches) == len(coordinates):
                for coord in coordinates:
                    image[coord] = "0"

    return len([c for c in "".join(["".join(line) for line in image]) if c == "#"])


def main():
    tiles = data()
    sides = int(math.sqrt(len(tiles)))
    solution = solve(tiles, [], sides)
    print(
        int(solution[0].tile.id)
        * int(solution[sides - 1].tile.id)
        * int(solution[len(tiles) - sides].tile.id)
        * int(solution[len(tiles) - 1].tile.id)
    )

    images = to_images(solution)
    res = [find_monsters(image) for image in images]
    print(min(res), res)


main()
