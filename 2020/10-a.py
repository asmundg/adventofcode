import functools


def update(d, pair):
    key = pair[1] - pair[0]
    d[key] = d.get(key, 0) + 1
    return d


with open("input/10.input") as f:
    nums = sorted([int(num) for num in f.readlines()])
    pairs = zip([0] + nums, nums + [max(nums) + 3])
    diffs = functools.reduce(update, pairs, dict())

    print(diffs[1] * diffs[3])
