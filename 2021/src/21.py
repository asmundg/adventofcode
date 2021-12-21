"""Very straight forward part 1 (just remember to zero-index
everything to make the modulu less complicated (and then increase the
score calculation by one to compensate)).

Part 2 clearly doesn't scale if we compute all permutations. Instead,
we can leverage the fact that the solution space is a prunable tree:
Any subtrees for (player, positions, scores) will always yield the
same win distribution, meaning we can cache and reuse the result,
skipping the entire subtree.

Given the low number of permutations, in these variables, this means
we quickly exhaust the solution space.

"""

import copy
import os


def read_data(fname):
    with open(fname, encoding="utf-8") as handle:
        return parse(handle.readlines())


def parse(lines):
    return [int(line.strip()[-1]) - 1 for line in lines]


def die_generator():
    i = 0
    while True:
        yield i + 1
        i = (i + 1) % 100


def solve(positions):
    die = die_generator()
    scores = [0, 0]
    player = 0
    throws = 0
    while True:
        throws += 3
        total = sum([die.__next__(), die.__next__(), die.__next__()])
        positions[player] = (positions[player] + total) % 10
        scores[player] += positions[player] + 1
        if scores[player] >= 1000:
            print(min(scores) * throws)
            return
        player = (player + 1) % 2


def dirac_universes():
    sums = {}
    for a in range(1, 4):
        for b in range(1, 4):
            for c in range(1, 4):
                t = sum([a, b, c])
                sums.setdefault(t, 0)
                sums[t] += 1
    return sums


DIRAC_OUTCOMES = dirac_universes()


def solve2(positions):
    print(max(play(positions, [0, 0], 0, 0, {}).values()))


def play(old_positions, old_scores, player, depth, cache):
    wins = {0: 0, 1: 0}

    cache_key = (
        player,
        (old_positions[0], old_positions[1]),
        (old_scores[0], old_scores[1]),
    )
    if cache_key in cache:
        return cache[cache_key]

    for steps, outcomes in DIRAC_OUTCOMES.items():
        positions = copy.deepcopy(old_positions)
        scores = copy.deepcopy(old_scores)
        positions[player] = (positions[player] + steps) % 10
        scores[player] += positions[player] + 1
        if scores[player] >= 21:
            wins[player] += outcomes
        else:
            new_wins = play(positions, scores, (player + 1) % 2, depth + 1, cache)
            for i in range(2):
                wins[i] += new_wins[i] * outcomes

    cache[cache_key] = wins
    return wins


solve(read_data(os.path.join(os.path.dirname(__file__), "input/21.test")))
solve(read_data(os.path.join(os.path.dirname(__file__), "input/21.input")))

solve2(read_data(os.path.join(os.path.dirname(__file__), "input/21.test")))
solve2(read_data(os.path.join(os.path.dirname(__file__), "input/21.input")))
