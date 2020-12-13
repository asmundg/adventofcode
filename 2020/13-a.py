def data():
    with open("input/13.input") as f:
        target = int(f.readline())
        ids = [int(bus_id) for bus_id in f.readline().split(",") if bus_id != "x"]
        return (target, ids)


def main():
    target, ids = data()
    values = {bus_id * (target / bus_id + 1): bus_id for bus_id in ids}

    departure = min(values.keys())
    bus = values[departure]
    diff = (departure - target) * bus
    print(diff, bus, values)


main()
