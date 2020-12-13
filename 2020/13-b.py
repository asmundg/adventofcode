def data():
    with open("input/13.input") as f:
        f.readline()
        ids = f.readline().split(",")
        return sorted(
            [(int(bus_id), ids.index(bus_id)) for bus_id in ids if bus_id != "x"],
            key=lambda a: a[0],
            reverse=True,
        )


def neat_offset(search, ids):
    for bus_id, i in ids:
        if (search + i) % bus_id != 0:
            return False
    return True


def period(ids, start, step):
    print(ids, start, step)

    search = start
    while True:
        if neat_offset(search, ids):
            break
        search += step
    a = search

    search += step
    while True:
        if neat_offset(search, ids):
            break
        search += step
    b = search

    return a, b - a


def main():
    ids = data()
    print(ids)

    start, step = 0, 1
    for i in range(2, len(ids) + 1):
        start, step = period(ids[:i], start, step)
        print(start, step)

    print(start)


main()
