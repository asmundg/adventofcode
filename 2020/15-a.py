def update(seen, number, generation):
    new = (
        seen[number][-1] - seen[number][0]
        if number in seen and len(seen[number]) == 2
        else 0
    )
    seen[new] = (seen[new][-1], generation) if new in seen else (generation,)
    print(number, new, seen)
    return new


def main():
    seen = {}
    initial = [19, 0, 5, 1, 10, 13]
    last = 0
    for i, num in enumerate(initial):
        seen[num] = (i,)
        last = num

    for i in range(len(initial), 2020):
        last = update(seen, last, i)

    print(last)


main()
