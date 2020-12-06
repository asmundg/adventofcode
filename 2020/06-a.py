import functools

with open("input/06.input") as f:
    sets = [set(line.replace("\n", "")) for line in f.read().strip().split("\n\n")]
    print(sets)
    print(sum([len(s) for s in sets]))
