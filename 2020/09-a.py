preamble = 25


def recalculate(numbers):
    deps = set()
    for a in numbers:
        for b in numbers:
            if a != b:
                deps.add(a + b)
    return deps


with open("input/09.input") as f:
    numbers = [int(num) for num in f.readlines()]
    window = numbers[0:preamble]
    deps = recalculate(window)

    for num in numbers[preamble:]:
        print(num, deps)
        if num in deps:
            window.append(num)
            window.pop(0)
            deps = recalculate(window)
        else:
            print(num)
            break
