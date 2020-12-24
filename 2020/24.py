def data():
    with open("input/24.input") as f:
        tiles = []
        for line in f.readlines():
            chars = [char for char in line.strip()]
            tiles.append([])
            while chars:
                char0 = chars.pop(0)
                if char0 in ("e", "w"):
                    tiles[-1].append(char0)
                else:
                    char1 = chars.pop(0)
                    tiles[-1].append(char0 + char1)
        return tiles


DIRECTIONS = {
    "e": (1, 0),
    "se": (1, -1),
    "sw": (0, -1),
    "w": (-1, 0),
    "nw": (-1, 1),
    "ne": (0, 1),
}


def tile_coordinate(tile):
    coordinate = (0, 0)
    for step in tile:
        coordinate = (
            coordinate[0] + DIRECTIONS[step][0],
            coordinate[1] + DIRECTIONS[step][1],
        )
    return coordinate


def neighbour_coordinates(coordinate):
    return [
        (coordinate[0] + step[0], coordinate[1] + step[1])
        for step in DIRECTIONS.values()
    ]


def place_tiles(tiles):
    floor = set()
    for tile in tiles:
        coordinate = tile_coordinate(tile)
        if coordinate in floor:
            floor.remove(coordinate)
        else:
            floor.add(coordinate)
    return floor


def iterate(tiles):
    new_tiles = set()
    for tile in tiles:
        neighbours = neighbour_coordinates(tile)
        if 0 < len([c for c in neighbours if c in tiles]) <= 2:
            new_tiles.add(tile)

        for neighbour in neighbours:
            if (
                neighbour not in tiles
                and len([c for c in neighbour_coordinates(neighbour) if c in tiles])
                == 2
            ):
                new_tiles.add(neighbour)

    return new_tiles


def iterate_tiles(tiles, iterations):
    for _ in range(iterations):
        tiles = iterate(tiles)
    return tiles


def main():
    print(len(place_tiles(data())))
    print(len(iterate_tiles(place_tiles(data()), 100)))


main()
