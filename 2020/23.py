import functools


class Cup:
    def __init__(self, value):
        self.value = value
        self.next = None


def move(current, cups):
    a, b, c, = (
        current.next,
        current.next.next,
        current.next.next.next,
    )
    current.next = c.next

    destination_val = (current.value - 1) or len(cups)
    while destination_val in set((a.value, b.value, c.value)):
        destination_val = destination_val - 1 or len(cups)

    destination = cups[destination_val]
    c.next = destination.next
    destination.next = a

    return current.next


def game(current, cups, iterations):
    for n in range(iterations):
        if n % 100000 == 0:
            print(n)
        current = move(current, cups)
    return current


# string of ints to Cup linked list, returning first element.
def prep(data, pad):
    cups = {}

    def update(last, cur):
        new = Cup(cur)
        cups[new.value] = new
        if last:
            last.next = new
        return new

    initial = Cup(0)
    nums = [int(num) for num in data]
    last = functools.reduce(
        update, nums + [n for n in range(max(nums) + 1, pad + 1)], initial
    )
    first = initial.next
    # Close the loop
    last.next = first
    return first, cups


def serialize(first):
    res = ""
    cur = first.next
    while cur != first:
        res += str(cur.value)
        cur = cur.next
    return res


def main():
    (part1_first, part1_cups) = prep("157623984", 0)
    game(part1_first, part1_cups, 100)

    (part2_first, part2_cups) = prep("157623984", 1000000)
    game(part2_first, part2_cups, 10000000)
    a, b = part2_cups[1].next.value, part2_cups[1].next.next.value

    print(serialize((part1_cups[1])))
    print(a, b, a * b)


main()
