"""Day 18

This is a bin graph. Explode/spit should just be repeated walks until
we have no changes. 

Explode is a bit annoying, since we need to track our position and
then traverse to find the previous and next leaf nodes. Abusing
exceptions lets us back out of call stacks instead of passing more
state around. Exceptions also make the repeated applicaton of explode
and split until stability very simple to express, albeit a bit costly.
"""
import copy
import math
import os


class Done(Exception):
    pass


class Rerun(Exception):
    pass


class Explode(Exception):
    def __init__(self, pos):
        self.pos = pos


def read_data(fname):
    with open(fname, encoding="utf-8") as handle:
        nums = []
        for line in [line.strip() for line in handle.readlines()]:
            nums.append(parse(line, 0))
        return nums


def parse(line, pos):
    if line[pos] == "[":
        # subgraph
        left, pos = parse(line, pos + 1)
    else:
        # literal
        left, pos = int(line[pos]), pos + 1

    # This was the top node
    if pos == len(line):
        return left

    assert line[pos] == ",", f"{line} {pos} {line[pos]}"
    pos += 1
    if line[pos] == "[":
        # Subgraph
        right, pos = parse(line, pos + 1)
    else:
        # literal
        right, pos = int(line[pos]), pos + 1
    assert line[pos] == "]", f"{line} {pos} {line[pos]}"
    return {"left": left, "right": right}, pos + 1


def solve(nums):
    cur = nums[0]
    for num in nums[1:]:
        cur = reduce({"left": cur, "right": num})
    return magnitude(cur)


def solve2(nums):
    largest = 0
    for num_a in nums:
        for num_b in nums:
            if num_a == num_b:
                continue

            mag = solve([copy.deepcopy(num_a), copy.deepcopy(num_b)])
            if mag > largest:
                largest = mag

    print(largest)


def magnitude(node):
    return (
        node
        if type(node) is int
        else (3 * magnitude(node["left"])) + (2 * magnitude(node["right"]))
    )


def reduce(node):
    while True:
        try:
            explode(node, -1, 0, node)
            split(node)
        except Rerun:
            pass
        else:
            break

    return node


def explode(node, pos, depth, root):
    # Leaf node, no eplosion
    if type(node) is int:
        return pos + 1

    # This is a literal pair, and we're too deep
    if depth >= 4 and type(node["left"]) is int and type(node["right"]) is int:
        try:
            inc(root, -1, pos, node["left"]) if pos >= 0 else None
        except Done:
            pass

        try:
            inc(root, -1, pos + 3, node["right"])
        except Done:
            pass

        # Just throw an exception, to let our parent replace us with a
        # 0.
        raise Explode(pos)

    try:
        pos = explode(node["left"], pos, depth + 1, root)
    except Explode as e:
        node["left"] = 0
        raise Rerun()

    try:
        pos = explode(node["right"], pos, depth + 1, root)
    except Explode as e:
        node["right"] = 0
        raise Rerun()

    return pos


def inc(node, pos, target, num):
    if type(node) is int:
        return pos + 1

    pos = inc(node["left"], pos, target, num)

    # Our left child is the target posppp
    if pos == target:
        node["left"] += num
        raise Done()

    pos = inc(node["right"], pos, target, num)

    # Our right child is the target pos
    if pos == target:
        node["right"] += num
        raise Done()

    return pos


def split(node):
    # Literal, no split
    if type(node) is int:
        return

    if type(node["left"]) is int and node["left"] >= 10:
        node["left"] = {
            "left": math.floor(node["left"] / 2),
            "right": math.ceil(node["left"] / 2),
        }
        raise Rerun()

    split(node["left"])

    if type(node["right"]) is int and node["right"] >= 10:
        node["right"] = {
            "left": math.floor(node["right"] / 2),
            "right": math.ceil(node["right"] / 2),
        }
        raise Rerun()

    split(node["right"])


print(solve(read_data(os.path.join(os.path.dirname(__file__), "input/18.test"))))
print(solve(read_data(os.path.join(os.path.dirname(__file__), "input/18.input"))))

solve2(read_data(os.path.join(os.path.dirname(__file__), "input/18.test")))
solve2(read_data(os.path.join(os.path.dirname(__file__), "input/18.input")))
