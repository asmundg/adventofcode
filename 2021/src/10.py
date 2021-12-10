import os


def read_data(fname):
    with open(fname, encoding="utf-8") as handle:
        return [line.strip() for line in handle.readlines()]


def solve(data):
    score = 0
    for line in data:
        score += check_line(line)
    print(score)


def check_line(line):
    scores = {")": 3, "]": 57, "}": 1197, ">": 25137}
    match = {")": "(", "]": "[", "}": "{", ">": "<"}
    stack = []

    for char in line:
        if char in match.keys():
            if stack[-1] == match[char]:
                stack.pop()
            else:
                return scores[char]
        else:
            stack.append(char)

    return 0


def solve2(data):
    incomplete_lines = [line for line in data if check_line(line) == 0]

    scores = [complete_line(line) for line in incomplete_lines]
    print(sorted(scores)[len(scores) // 2])


def complete_line(line):
    scores = {"(": 1, "[": 2, "{": 3, "<": 4}
    match = {")": "(", "]": "[", "}": "{", ">": "<"}

    stack = []

    for char in line:
        if char in match.keys():
            stack.pop()
        else:
            stack.append(char)

    score = 0
    while stack:
        char = stack.pop()
        score = score * 5 + scores[char]
    return score


solve(read_data(os.path.join(os.path.dirname(__file__), "input/10.test")))
solve(read_data(os.path.join(os.path.dirname(__file__), "input/10.input")))

solve2(read_data(os.path.join(os.path.dirname(__file__), "input/10.test")))
solve2(read_data(os.path.join(os.path.dirname(__file__), "input/10.input")))
