"""Oh wow.

This is logically very similar to Dijkstra/A*, pruning search trees
based on the cheapest way to get to a certain permutation. We can both
throw away subtrees if there is a cheaper way to get to them and if
we're above the cheapest known completion. I feel like I'm missing
some heuristic for selecting the best moves though, so we still end up
trying _a lot_ of combinations.
"""
import copy


def solve(data):
    print(walk(data, depth=2))


def solve2(data):
    print(walk(data, depth=4))


COST = {"A": 1, "B": 10, "C": 100, "D": 1000}


def available_moves(pos, occupied, depth=2):
    # Can't move
    if pos[1] > 1 and (pos[0], pos[1] - 1) in occupied:
        return []

    target_x = ("ABCD".index(occupied[pos]) + 1) * 2

    # In the right bucket
    if pos[0] == target_x and not [
        p
        for p in occupied
        if p[0] == pos[0] and p[1] > pos[1] and occupied[p] != occupied[pos]
    ]:
        return []

    # Free movement corridor
    lo_x = 0
    hi_x = 10
    for p in occupied:
        if p[1] == 0:
            if p[0] >= lo_x and p[0] < pos[0]:
                lo_x = p[0] + 1
            if p[0] <= hi_x and p[0] > pos[0]:
                hi_x = p[0] - 1

    # Can move to target bucket?
    if lo_x <= target_x <= hi_x:
        moves = []
        for y in range(depth, 0, -1):
            if not (target_x, y) in occupied:
                return [(target_x, y)]
            if occupied[(target_x, y)] != occupied[pos]:
                break
        else:
            return moves

    # If in hallway, can't move if target bucket isn't open
    if pos[1] == 0:
        return []

    return [
        (x, 0) for x in range(lo_x, hi_x + 1) if (x % 2 or x in (0, 10)) and x != pos[0]
    ]


def in_right_place(pos, occupied):
    if pos[0] < 2 or pos[0] > 8:
        return False

    target_x = ("ABCD".index(occupied[pos]) + 1) * 2
    return pos[0] == target_x and not [
        p
        for p in occupied
        if p[0] == pos[0] and p[1] > pos[1] and occupied[p] != occupied[pos]
    ]


def walk(occupied, depth=2):
    search = [(occupied, 0)]
    best = {}
    best_end = 99999999999999

    while search:
        occupied, score = search.pop(-1)
        for pos, shrimp in occupied.items():
            for move in available_moves(pos, occupied, depth):
                new_occupied = copy.deepcopy(occupied)
                del new_occupied[pos]
                assert move != pos
                new_occupied[move] = shrimp
                new_score = score + COST[shrimp] * (
                    # x movement
                    abs(move[0] - pos[0])
                    # y movement
                    + (pos[1] + move[1])
                )

                done = False not in [
                    in_right_place(pos, new_occupied) for pos in new_occupied
                ]
                if done:
                    if new_score < best_end:
                        best_end = new_score
                    continue

                key = cache_key(new_occupied)
                if (key in best and best[key] <= new_score) or best_end <= new_score:
                    continue

                best[key] = new_score
                search.append((new_occupied, new_score))

    return best_end


def cache_key(occupied):
    return "".join(str(key) + str(occupied[key]) for key in sorted(occupied))


if __name__ == "__main__":
    solve(
        {
            (2, 1): "B",
            (2, 2): "A",
            (4, 1): "C",
            (4, 2): "D",
            (6, 1): "B",
            (6, 2): "C",
            (8, 1): "D",
            (8, 2): "A",
        },
    )
    solve(
        {
            (2, 1): "C",
            (2, 2): "C",
            (4, 1): "B",
            (4, 2): "D",
            (6, 1): "A",
            (6, 2): "A",
            (8, 1): "D",
            (8, 2): "B",
        },
    )

    solve2(
        {
            (2, 1): "B",
            (2, 2): "D",
            (2, 3): "D",
            (2, 4): "A",
            (4, 1): "C",
            (4, 2): "C",
            (4, 3): "B",
            (4, 4): "D",
            (6, 1): "B",
            (6, 2): "B",
            (6, 3): "A",
            (6, 4): "C",
            (8, 1): "D",
            (8, 2): "A",
            (8, 3): "C",
            (8, 4): "A",
        },
    )
    solve2(
        {
            (2, 1): "C",
            (2, 2): "D",
            (2, 3): "D",
            (2, 4): "C",
            (4, 1): "B",
            (4, 2): "C",
            (4, 3): "B",
            (4, 4): "D",
            (6, 1): "A",
            (6, 2): "B",
            (6, 3): "A",
            (6, 4): "A",
            (8, 1): "D",
            (8, 2): "A",
            (8, 3): "C",
            (8, 4): "B",
        },
    )
