"""Day 05:"""

import os
from textwrap import dedent


def read_data() -> str:
    day = os.path.basename(__file__).split(".")[0].split("_")[1]
    fname = os.path.join(os.path.dirname(__file__), "input", f"{day}.input")

    with open(fname, encoding="utf-8") as handle:
        return handle.read().strip()


def parse(data: str) -> list[tuple[int, int]]:
    coords = []
    for line in data.split("\n"):
        a, b = line.split(", ")
        coords.append((int(a), int(b)))
    return coords


def distance(a: tuple[int, int], b: tuple[int, int]) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def neighbours(a: tuple[int, int]) -> list[tuple[int, int]]:
    return [(a[0] - 1, a[1]), (a[0] + 1, a[1]), (a[0], a[1] - 1), (a[0], a[1] + 1)]


def part1(coords: list[tuple[int, int]]) -> int:
    search = coords[:]
    visited = set(search)
    areas = {k: 1 for k in coords}
    inf = set()

    while search:
        point = search.pop()
        for n in neighbours(point):
            if n in visited:
                continue
            visited.add(n)

            prev_distances = [distance(point, c) for c in coords]
            distances = [distance(n, c) for c in coords]

            equidistant_n = [i for i, dist in enumerate(distances) if dist == min(distances)]

            # inf
            if all([d > p for d, p in zip(distances, prev_distances)]):
                if len(equidistant_n) == 1:
                    inf.add(coords[equidistant_n[0]])
                continue

            if distances.count(min(distances)) == 1:
                closest = coords[distances.index(min(distances))]
                if closest in areas:
                    areas[closest] += 1

            search.append(n)

    [v for k, v in areas.items() if k not in inf]
    return sorted([v for k, v in areas.items() if k not in inf])[-1]


def part2(coords: list[tuple[int, int]], max_dist: int = 10000) -> int:
    search = coords[:]
    visited = {}

    while search:
        point = search.pop()
        visited[point] = sum([distance(point, c) for c in coords])

        for n in neighbours(point):
            if n in visited:
                continue

            total_distance = sum([distance(n, c) for c in coords])
            if total_distance < max_dist:
                search.append(n)

    return len([v for v in visited.values() if v < max_dist])


def test_part1():
    data = dedent(
        """
        1, 1
        1, 6
        8, 3
        3, 4
        5, 5
        8, 9
        """
    ).strip()
    assert part1(parse(data)) == 17


def test_part2():
    data = dedent(
        """
        1, 1
        1, 6
        8, 3
        3, 4
        5, 5
        8, 9
        """
    ).strip()
    assert part2(parse(data), 32) == 16


if __name__ == "__main__":
    print(part1(parse(read_data())))
    print(part2(parse(read_data())))
