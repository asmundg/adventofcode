cache = {}


def walk(nums, pos, end):
    if pos == len(nums) - 1:
        return 1

    next_pos = pos + 1
    total = 1 if end - nums[pos] <= 3 else 0
    while next_pos < len(nums) and nums[next_pos] - nums[pos] <= 3:
        if next_pos not in cache:
            cache[next_pos] = walk(nums, next_pos, end)
        total += cache[next_pos]
        next_pos += 1
    return total


with open("input/10.input") as f:
    data = sorted([int(num) for num in f.readlines()])

    print(walk([0] + data, 0, max(data) + 3))
