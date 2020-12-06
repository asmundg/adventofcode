import functools


def intersection(group):
    return len(
        functools.reduce(
            lambda acc, cur: acc.intersection(set(cur)), group, set(group[0])
        )
    )


with open("input/06.input") as f:
    all = [line.split("\n") for line in f.read().strip().split("\n\n")]
    groups = [intersection(group) for group in all]
    print(groups)
    print(sum(groups))
