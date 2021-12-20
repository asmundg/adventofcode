"""The trick here is that we need to account for how the infinite
blackness looks, since the pixel correction for "empty" can end up
flipping the bit.

Once we track how empty looks (by enhancing an empty image each
iteration), we can use that pixel to fill in values beyond the edge of
the image when enhancing.

We also need to ensure that we always have an empty border around the
image, since those pixels can get populated by the enhancement
algorithm. Thus, every time we don't have an empty border, we need to
grow the image to include more empty space.

There's some very inefficient reallocation of lists here, but who
cares. :P

"""
import copy
import os


def read_data(fname):
    with open(fname, encoding="utf-8") as handle:
        correction = handle.readline().strip()
        handle.readline()
        return [[c for c in line.strip()] for line in handle.readlines()], correction


def find_neighbours(y, x, image, pad):
    return [
        [
            image[y - 1][x - 1] if y > 0 and x > 0 else pad,
            image[y - 1][x] if y > 0 else pad,
            image[y - 1][x + 1] if y > 0 and x < (len(image[0]) - 1) else pad,
        ],
        [
            image[y][x - 1] if x > 0 else pad,
            image[y][x],
            image[y][x + 1] if x < (len(image[0]) - 1) else pad,
        ],
        [
            image[y + 1][x - 1] if y < (len(image) - 1) and x > 0 else pad,
            image[y + 1][x] if y < (len(image) - 1) else pad,
            image[y + 1][x + 1]
            if y < len(image) - 1 and x < (len(image[0]) - 1)
            else pad,
        ],
    ]


def pad_out(image, inf):
    pad_row = [inf] * len(image[0])
    image.insert(0, pad_row)
    image.append(pad_row)

    for i, row in enumerate(image):
        image[i] = [inf] + row + [inf]

    return image


def needs_pad(image, inf_value):
    return (
        image[0] != [inf_value] * len(image[0])
        or image[-1] != [inf_value] * len(image[0])
        or [row[0] for _, row in enumerate(image)] != [inf_value] * len(image)
        or [row[-1] for _, row in enumerate(image)] != [inf_value] * len(image)
    )


def enhance(image, correction, pad):
    enhanced = copy.deepcopy(image)
    for y, row in enumerate(image):
        for x, _ in enumerate(row):
            neighbours = find_neighbours(y, x, image, pad)
            code = "".join(c for n in neighbours for c in n)
            enhanced[y][x] = correction[
                int(code.replace(".", "0").replace("#", "1"), 2)
            ]

    return enhanced


def printable(image):
    return "\n".join(["".join(line) for line in image])


def solve(args, steps=2):
    image, correction = args
    inf = [["." for _ in range(3)] for _ in range(3)]

    for _ in range(steps):
        if needs_pad(image, inf[1][1]):
            image = pad_out(image, inf[1][1])

        image = enhance(image, correction, inf[1][1])
        inf = enhance(inf, correction, inf[1][1])

    complete = printable(image)
    print(complete)
    print(len([c for c in complete if c == "#"]))


solve(read_data(os.path.join(os.path.dirname(__file__), "input/20.test")))
solve(read_data(os.path.join(os.path.dirname(__file__), "input/20.input")))

solve(
    read_data(os.path.join(os.path.dirname(__file__), "input/20.test")),
    steps=50,
)
solve(
    read_data(os.path.join(os.path.dirname(__file__), "input/20.input")),
    steps=50,
)
