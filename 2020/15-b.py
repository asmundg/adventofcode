def update(seen, number, generation):
    new = (
        seen[number][-1] - seen[number][0]
        if number in seen and len(seen[number]) == 2
        else 0
    )
    seen[new] = (seen[new][-1], generation) if new in seen else (generation,)
    return new


def main():
    seen = {}
    initial = [19, 0, 5, 1, 10, 13]
    last = 0
    for i, num in enumerate(initial):
        seen[num] = (i,)
        last = num

    for i in range(len(initial), 30000000):
        if i % 100000 == 0:
            print(i)
        last = update(seen, last, i)

    print(last)


main()
