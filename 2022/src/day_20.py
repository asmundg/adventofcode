"""Day 20: Grove Positioning System

Aka linked lists are surprisingly hard to get right. Especially when
one forgets to remove the current node before finding the new
position.

Realizing that finding a high index moodulo the length of the mixed
sequence is trivial if we sort the array first meant part 2 was
trivial, as incrementing or decrementing arbitrary numbers doesn't
cause additional cost, as compared to following the linked list.

"""

import os


def parse(fname):
    with open(fname, encoding="utf-8") as handle:
        nums = [{"num": int(line)} for line in handle.read().strip().split("\n")]
        for a, b in zip(nums, nums[1:]):
            a["next"] = b
            b["prev"] = a
        nums[0]["prev"] = nums[-1]
        nums[-1]["next"] = nums[0]
        return nums


def reindex(nums):
    """
    Create new list starting at 0 and ordered by link sequence
    """
    c = 0
    p = nums[0]
    while p["num"] != 0:
        if c > len(nums):
            raise Exception("Infinite loop")
        p = p["next"]
        c += 1

    start = p
    indexed = []
    while True:
        indexed.append(p)
        p = p["next"]
        if p is start:
            break

    return indexed


def mix(nums):
    for i, num in enumerate(nums):
        if num["num"] == 0:
            continue

        indexed = reindex(nums)
        pointer_index = next((i for i, pointer in enumerate(indexed) if pointer is num))

        # remove
        num["next"]["prev"] = num["prev"]
        num["prev"]["next"] = num["next"]
        indexed = reindex(nums)
        pointer = indexed[(pointer_index + num["num"] - 1) % len(indexed)]

        num["next"] = pointer["next"]
        num["prev"] = pointer
        num["next"]["prev"] = num
        pointer["next"] = num

        assert len(reindex(nums)) == len(nums)

    return nums


def solve1(fname: str):
    nums = reindex(mix(parse(fname)))
    return sum([nums[n % len(nums)]["num"] for n in range(1000, 3000 + 1, 1000)])


def solve2(fname: str):
    nums = parse(fname)
    for num in nums:
        num["num"] *= 811589153

    for _ in range(10):
        nums = mix(nums)
    indexed = reindex(nums)
    return sum([indexed[n % len(nums)]["num"] for n in range(1000, 3000 + 1, 1000)])


day = os.path.basename(__file__).split(".")[0].split("_")[1]
base = os.path.join(os.path.dirname(__file__), "input", f"{day}")

print(solve1(f"{base}.test"))
print(solve1(f"{base}.input"))

print(solve2(f"{base}.test"))
print(solve2(f"{base}.input"))
