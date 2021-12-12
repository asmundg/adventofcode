import os
import re


def read_data(fname):
    graph = {}
    with open(fname, encoding="utf-8") as handle:
        for line in [line.strip() for line in handle.readlines()]:
            a, b = line.split("-")
            graph.setdefault(a, []).append(b)
            graph.setdefault(b, []).append(a)
    return graph


def solve(graph):
    print(len(walk("start", [], graph)))


def walk(node, path, graph):
    if re.match("[a-z]+", node) and node in path:
        return []

    if node == "end":
        return [path[:] + [node]]

    return [
        complete_path
        for connection in graph[node]
        for complete_path in walk(connection, path[:] + [node], graph)
        if complete_path
    ]


def solve2(graph):
    print(len(walk2("start", [], graph, False)))


def walk2(node, path, graph, used_quota):
    if re.match("[a-z]+", node) and node in path:
        if used_quota or node in ("start", "end"):
            return []
        used_quota = True

    if node == "end":
        return [path[:] + [node]]

    return [
        complete_path
        for connection in graph[node]
        for complete_path in walk2(connection, path[:] + [node], graph, used_quota)
        if complete_path
    ]


solve(read_data(os.path.join(os.path.dirname(__file__), "input/12.test")))
solve(read_data(os.path.join(os.path.dirname(__file__), "input/12.input")))

solve2(read_data(os.path.join(os.path.dirname(__file__), "input/12.test")))
solve2(read_data(os.path.join(os.path.dirname(__file__), "input/12.input")))
