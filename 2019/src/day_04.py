"""Secure Container

For all numbers in a range, how many satisfy some criteria?

We could probably reduce the search space a lot by skipping all
numbers where the digits aren't strictly increasing. But the search
space is so small in any case that we really don't have to care.
"""


def parse(line):
    return [int(n) for n in line.split("-")]


def solve(a, b, loose=True):
    candidates = 0
    for i in range(a, b):
        s = str(i)
        last = s[0]
        counts = {last: 0}
        for char in s:
            if char < last:
                break

            if char == last:
                counts[char] += 1
            else:
                counts[char] = 1

            last = char
        else:
            if (loose and max(counts.values()) >= 2) or 2 in counts.values():
                candidates += 1
    return candidates


def test_something():
    assert False


if __name__ == "__main__":
    print(solve(*parse("152085-670283")))
    print(solve(*parse("152085-670283"), loose=False))
