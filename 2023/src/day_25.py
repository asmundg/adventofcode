"""Day 25: Snowverload

Another day where graphviz allows us to trivially visually identify
the crux edges that we can remove to split the graph.

Then it's a trivial flood fill to find the sizes of the two halves.

"""

import os
from typing import List, Dict


def read_data() -> str:
    day = os.path.basename(__file__).split(".")[0].split("_")[1]
    fname = os.path.join(os.path.dirname(__file__), "input", f"{day}.input")

    with open(fname, encoding="utf-8") as handle:
        return handle.read().strip()


def parse(data: str):
    nodes: Dict[str, List[str]] = {}

    for line in data.split("\n"):
        src, dest = line.split(": ")
        for dst in dest.split(" "):
            nodes.setdefault(src, []).append(dst)
            nodes.setdefault(dst, []).append(src)

    return nodes


def part1(data: str) -> int:
    nodes = parse(data)

    # Hard coded connections to sever, visually identified via
    # graphviz
    sever_connections = (("pzr", "sss"), ("njx", "pbx"), ("sxx", "zvk"))
    for src, dst in sever_connections:
        nodes[src].remove(dst)
        nodes[dst].remove(src)

    def flood(nodes, start):
        found = set()
        search = {start}
        while search:
            node = search.pop()
            for connection in nodes[node]:
                if connection not in found:
                    found.add(connection)
                    search.add(connection)
        return found

    return len(flood(nodes, sever_connections[0][0])) * len(
        flood(nodes, sever_connections[0][1])
    )


if __name__ == "__main__":
    print(part1(read_data()))
