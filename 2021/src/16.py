import functools
import os


def read_data(fname):
    with open(fname, encoding="utf-8") as handle:
        return [line.strip() for line in handle.readlines()]


def solve(data):
    for line in data:
        binary = "".join(bin(int(char, 16))[2:].zfill(4) for char in line)

        num, versions, _ = parse_packet(0, binary)
        print(num, sum(versions))


def parse_packet(pointer, binary):
    version, pointer = read(3, pointer, binary)
    type_id, pointer = read(3, pointer, binary)

    if type_id == 4:
        num, pointer = parse_literal_packet(pointer, binary)
        return num, [version], pointer

    ops = {
        0: sum,
        1: lambda nums: functools.reduce(lambda acc, cur: acc * cur, nums, 1),
        2: min,
        3: max,
        5: lambda nums: 1 if nums[0] > nums[1] else 0,
        6: lambda nums: 1 if nums[0] < nums[1] else 0,
        7: lambda nums: 1 if nums[0] == nums[1] else 0,
    }

    num, versions, pointer = parse_operator_packet(pointer, binary, ops[type_id])
    return num, versions + [version], pointer


def parse_operator_packet(pointer, binary, op):
    mode, pointer = read(1, pointer, binary)
    nums_acc = []
    versions_acc = []

    if mode == 0:
        length, pointer = read(15, pointer, binary)
        end = pointer + length
        while pointer < end:
            num, versions, pointer = parse_packet(pointer, binary)
            nums_acc.append(num)
            versions_acc += versions
    elif mode == 1:
        count, pointer = read(11, pointer, binary)
        for _ in range(count):
            num, versions, pointer = parse_packet(pointer, binary)
            nums_acc.append(num)
            versions_acc += versions

    return op(nums_acc), versions_acc, pointer


def parse_literal_packet(pointer, binary):
    num = ""
    while True:
        num_part, pointer = read(5, pointer, binary, to_int=False)
        num += num_part[1:]
        if num_part[0] == "0":
            break
    num = int(num, 2)

    return num, pointer


def read(length, pointer, binary, to_int=True):
    value = binary[pointer : pointer + length]
    if to_int:
        value = int(value, 2)
    return value, pointer + length


solve(read_data(os.path.join(os.path.dirname(__file__), "input/16.test")))
solve(read_data(os.path.join(os.path.dirname(__file__), "input/16.input")))
