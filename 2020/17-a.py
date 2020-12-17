def get_data():
    cubes = set()
    z = 0
    with open("input/17.input") as f:
        for y, line in enumerate(f.readlines()):
            for x, char in enumerate(line.strip()):
                if char == "#":
                    cubes.add((x, y, z))
    return cubes


def iterate(state):
    new_state = set()
    for pos in state:
        neighbor_positions = neighbors(pos)
        active_neighbors = len(
            [neigh_pos for neigh_pos in neighbor_positions if neigh_pos in state]
        )
        if 2 <= active_neighbors <= 3:
            new_state.add(pos)
        for neigh_pos in neighbor_positions:
            if (
                neigh_pos not in state
                and sum(
                    1
                    for neigh_neigh_pos in neighbors(neigh_pos)
                    if neigh_neigh_pos in state
                )
                == 3
            ):
                new_state.add(neigh_pos)
    return new_state


def neighbors(pos):
    positions = set()
    for x in range(pos[0] - 1, pos[0] + 2):
        for y in range(pos[1] - 1, pos[1] + 2):
            for z in range(pos[2] - 1, pos[2] + 2):
                if (x, y, z) != (pos[0], pos[1], pos[2]):
                    positions.add((x, y, z))
    return positions


def main(state, cycles):
    for _ in range(cycles):
        state = iterate(state)
    return state


print(len(main(get_data(), 6)))
