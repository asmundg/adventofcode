"""Day 04:"""

import os


def read_data() -> str:
    day = os.path.basename(__file__).split(".")[0].split("_")[1]
    fname = os.path.join(os.path.dirname(__file__), "input", f"{day}.input")

    with open(fname, encoding="utf-8") as handle:
        return handle.read().strip()


def parse(data: str) -> dict[int, list[list[tuple[int, int]]]]:
    log = sorted(data.split("\n"))
    guards: dict[int, list[list[tuple[int, int]]]] = {}
    current_guard = -1
    for line in log:
        if "begins shift" in line:
            current_guard = int(line.split(" ")[3][1:])
            if current_guard not in guards:
                guards[current_guard] = []
            guards[current_guard].append([])
        if "falls asleep" in line:
            h, m = line.split(" ")[1].split(":")
            assert h == "00"
            asleep = int(m[:-1])
        if "wakes up" in line:
            h, m = line.split(" ")[1].split(":")
            assert h == "00"
            guards[current_guard][-1].append((asleep, int(m[:-1])))
    return guards


def part1(guards: dict[int, list[list[tuple[int, int]]]]) -> int:
    best_guard = -1
    longest_sleep = 0
    for guard, shifts in guards.items():
        sleep = 0
        for shift in shifts:
            for a, b in shift:
                sleep += b - a
        if sleep > longest_sleep:
            longest_sleep = sleep
            best_guard = guard

    buckets = {m: 0 for m in range(60)}
    for shift in guards[best_guard]:
        for a, b in shift:
            for minute in range(a, b):
                buckets[minute] += 1

    return best_guard * sorted(buckets, key=lambda k: buckets[k])[-1]


def part2(guards: dict[int, list[list[tuple[int, int]]]]) -> int:
    best_minute = -1
    best_guard = -1
    best_minute_frequency = -1
    for guard, shifts in guards.items():
        buckets = {m: 0 for m in range(60)}
        for shift in shifts:
            for a, b in shift:
                for minute in range(a, b):
                    buckets[minute] += 1

        best = sorted(buckets, key=lambda k: buckets[k])[-1]
        if buckets[best] > best_minute_frequency:
            best_minute_frequency = buckets[best]
            best_minute = best
            best_guard = guard
    return best_guard * best_minute


if __name__ == "__main__":
    print(part1(parse(read_data())))
    print(part2(parse(read_data())))
