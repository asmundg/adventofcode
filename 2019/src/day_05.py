"""Sunny with a Chance of Asteroids

No cleverness today.
"""
import os


def read_data(fname):
    with open(fname, encoding="utf-8") as handle:
        return parse(handle.readlines())


def parse(lines):
    return [int(num) for num in lines[0].split(",")]


def argument_vals(program, pointer, n):
    vals = []
    for i in range(1, n + 1):
        mode = program[pointer] // (10 ** (i + 1)) % 10
        vals.append(
            program[pointer + i] if mode == 1 else program[program[pointer + i]]
        )
    return pointer + n + 1, vals


def add(program, pointer, _state):
    res_addr = program[pointer + 3]
    pointer, (val0, val1, _) = argument_vals(program, pointer, 3)
    program[res_addr] = val0 + val1
    return pointer


def mul(program, pointer, _state):
    res_addr = program[pointer + 3]
    pointer, (val0, val1, _) = argument_vals(program, pointer, 3)
    program[res_addr] = val0 * val1
    return pointer


def read(program, pointer, state):
    res_addr = program[pointer + 1]
    pointer, _ = argument_vals(program, pointer, 1)
    program[res_addr] = state["input_source"].pop()
    return pointer


def write(program, pointer, _state):
    pointer, (val0,) = argument_vals(program, pointer, 1)
    print(val0)
    return pointer


def jump_if_true(program, pointer, _state):
    pointer, (val0, val1) = argument_vals(program, pointer, 2)
    return val1 if val0 else pointer


def jump_if_false(program, pointer, _state):
    pointer, (val0, val1) = argument_vals(program, pointer, 2)
    return val1 if not val0 else pointer


def lt(program, pointer, _state):
    res_addr = program[pointer + 3]
    pointer, (val0, val1, _) = argument_vals(program, pointer, 3)
    program[res_addr] = 1 if val0 < val1 else 0
    return pointer


def eq(program, pointer, _state):
    res_addr = program[pointer + 3]
    pointer, (val0, val1, _) = argument_vals(program, pointer, 3)
    program[res_addr] = 1 if val0 == val1 else 0
    return pointer


def hcf(_program, _pointer, _state):
    return -1


cpu = {
    1: add,
    2: mul,
    3: read,
    4: write,
    5: jump_if_true,
    6: jump_if_false,
    7: lt,
    8: eq,
    99: hcf,
}


def solve(program, state):
    pointer = 0
    while pointer != -1:
        pointer = step(program, pointer, state)


def step(program, pointer, state):
    if program[pointer] % 100 in cpu:
        return cpu[program[pointer] % 100](program, pointer, state)

    raise Exception(f"Invalid instruction@{pointer}: {program[pointer]}")


if __name__ == "__main__":
    solve(
        read_data(os.path.join(os.path.dirname(__file__), "input/05.input")),
        {"input_source": [1]},
    )
    solve(
        read_data(os.path.join(os.path.dirname(__file__), "input/05.input")),
        {"input_source": [5]},
    )
