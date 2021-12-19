"""Relatively straight forward vector manipulation, finding overlaps
is just a matter of calculating the rotations and comparing vectors to
all points for each pair of origin points.

Super expensive though, and I'm sure there is a lot of room for
optimization (like not re-calculating the rotations and vectors all the time.)

Not sure if there's some structural optimizations we could do. Looking
at all point pairs seems wasteful.

"""
import os


def find_rotations():
    """
    There's probably something I could reference here, but lets just
    calculate all possible coordinate permutations.
    """

    def neg(s):
        return s[1] if s[0] == "-" else f"-{s}"

    (x, y, z) = ("x", "y", "z")

    # rotate on z, clockwise
    rotations = set([(x, y, z)])
    rotations.add((y, neg(x), z))
    rotations.add((neg(x), neg(y), z))
    rotations.add((neg(y), x, z))

    # rotate on x, clockwise
    for (x, y, z) in rotations.copy():
        rotations.add((x, neg(z), y))
        rotations.add((x, neg(y), neg(z)))
        rotations.add((x, z, neg(y)))

    # rotate on y, clockwise:
    for (x, y, z) in rotations.copy():
        rotations.add((z, y, neg(x)))
        rotations.add((neg(x), y, neg(z)))
        rotations.add((neg(z), y, x))

    assert len(rotations) == 24, len(rotations)
    print(rotations)


def read_data(fname):
    scanners = []
    with open(fname, encoding="utf-8") as handle:
        for line in [line.strip() for line in handle.readlines()]:
            if line.startswith("---"):
                scanners.append([])
                continue
            if not line:
                continue
            scanners[-1].append(tuple(int(num) for num in line.split(",")))
    return scanners


def rotate(coord):
    (x, y, z) = coord
    return [
        (-x, -y, z),
        (-x, -z, -y),
        (-x, y, -z),
        (-x, z, y),
        (-y, -x, -z),
        (-y, -z, x),
        (-y, x, z),
        (-y, z, -x),
        (-z, -x, y),
        (-z, -y, -x),
        (-z, x, -y),
        (-z, y, x),
        (x, -y, -z),
        (x, -z, y),
        (x, y, z),
        (x, z, -y),
        (y, -x, z),
        (y, -z, -x),
        (y, x, -z),
        (y, z, x),
        (z, -x, -y),
        (z, -y, x),
        (z, x, y),
        (z, y, -x),
    ]


def rotate_scanner(coords):
    new_coords = [[] for i in range(24)]
    for coord in coords:
        for i, new_coord in enumerate(rotate(coord)):
            new_coords[i].append(new_coord)

    return new_coords


def subtract_point(a, b):
    return (b[0] - a[0], b[1] - a[1], b[2] - a[2])


def vectors(coord, coords):
    """Find all vectors to other coords from this coord"""
    return [subtract_point(coord, other) for other in coords]


def solve(scanners):
    # The first scanner is always "right", accumulate rotations that
    # overlap with it (or found overlapping rotations).
    known = scanners[0:1]
    search = known[:]
    remaining = scanners[1:]
    locations = []
    while remaining:
        print(len(known), len(remaining), len(search))
        corrected, old, new_locations = find_next(search.pop(), remaining)
        remaining = [scanner for scanner in remaining if scanner not in old]
        search += corrected
        known = known + corrected
        locations += new_locations

    print(len({point for scanner in known for point in scanner}))
    largest = 0
    for a in locations:
        for b in locations:
            distance = sum(abs(val) for val in subtract_point(a, b))
            if distance > largest:
                largest = distance
    print(largest)


def find_next(scanner_a, remaining):
    all_corrected = []
    all_old = []
    all_locations = []
    for b, scanner_b in enumerate(remaining):
        for b_i, b_rotation in enumerate(rotate_scanner(scanner_b)):
            result = correct_from_overlap(scanner_a, b_rotation)
            if result:
                corrected, location = result
                all_corrected.append(corrected)
                all_old.append(scanner_b)
                all_locations.append(location)

    return all_corrected, all_old, all_locations


def correct_from_overlap(scanner_a, scanner_b):
    for point_a in scanner_a:
        a_vectors = vectors(point_a, scanner_a)
        for point_b in scanner_b:
            b_vectors = vectors(point_b, scanner_b)
            overlaps = [vec for vec in a_vectors if vec in b_vectors]
            if len(overlaps) >= 12:
                correction_vector = subtract_point(point_a, point_b)
                # The scanner position, relative to origin, is the
                # inverted correction vector (it's as far from the
                # origin as the correction vector, but going the other
                # way)
                scanner_location = tuple(-value for value in correction_vector)
                return [
                    subtract_point(correction_vector, point) for point in scanner_b
                ], scanner_location


solve(read_data(os.path.join(os.path.dirname(__file__), "input/19.test")))
solve(read_data(os.path.join(os.path.dirname(__file__), "input/19.input")))
