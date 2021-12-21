import copy
import os


def read_data(fname):
    with open(fname, encoding="utf-8") as handle:
        return parse(handle.readlines())


def parse(lines):
    return [int(num) for num in lines[0].split(",")]


def solve(program):
    pointer = 0
    program[1] = 12
    program[2] = 2
    while pointer is not None:
        pointer = step(program, pointer)
    print(program[0])


def solve2(original_program):
    for a in range(100):
        for b in range(100):
            program = copy.deepcopy(original_program)
            pointer = 0
            program[1] = a
            program[2] = b
            while pointer is not None:
                pointer = step(program, pointer)
            if program[0] == 19690720:
                print(a, b, 100 * a + b)
                return


def step(program, pointer):
    if program[pointer] == 1:
        addr0 = program[pointer + 1]
        addr1 = program[pointer + 2]
        res_addr = program[pointer + 3]
        program[res_addr] = program[addr0] + program[addr1]
        pointer += 4
    elif program[pointer] == 2:
        addr0 = program[pointer + 1]
        addr1 = program[pointer + 2]
        res_addr = program[pointer + 3]
        program[res_addr] = program[addr0] * program[addr1]
        pointer += 4
    elif program[pointer] == 99:
        return
    else:
        raise Exception(program[pointer])

    return pointer


def test_something():
    program = [1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50]
    assert step(program, 0) == 4
    assert program == [
        1,
        9,
        10,
        70,
        2,
        3,
        11,
        0,
        99,
        30,
        40,
        50,
    ]
    assert step(program, 4) == 8
    assert program == [3500, 9, 10, 70, 2, 3, 11, 0, 99, 30, 40, 50]

    assert step(program, 8) is None


if __name__ == "__main__":
    solve(read_data(os.path.join(os.path.dirname(__file__), "input/02.input")))
    solve2(read_data(os.path.join(os.path.dirname(__file__), "input/02.input")))
