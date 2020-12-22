def data():
    with open("input/22.input") as f:
        f.readline()
        player1 = []
        line = f.readline().strip()
        while line:
            player1.append(int(line))
            line = f.readline().strip()

        f.readline()
        player2 = []
        line = f.readline().strip()
        while line:
            player2.append(int(line))
            line = f.readline().strip()

        return (player1, player2)


def game(players, recursive):
    seen = set()

    while players[0] and players[1]:
        players = round(players, recursive)

        key = str(players)
        if key in seen:
            return ([1], [])
        seen.add(key)

    return players


def round(players, recursive):
    player1, player2 = players
    card1, card2 = player1.pop(0), player2.pop(0)

    winner = 0 if card1 > card2 else 1
    if recursive and card1 <= len(player1) and card2 <= len(player2):
        winner = 0 if game((player1[:card1], player2[:card2]), recursive + 1)[0] else 1

    return (
        (player1 + [card1, card2], player2)
        if winner == 0
        else (player1, player2 + [card2, card1])
    )


def score(player):
    return sum(i * num for i, num in enumerate(reversed(player), 1))


def main():
    players = data()
    part1 = game(players, recursive=0)
    print([score(player) for player in part1])

    print("PART2")
    players = data()
    part2 = game(players, recursive=1)
    print([score(player) for player in part2])


main()
