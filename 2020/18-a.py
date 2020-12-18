def data():
    with open("input/18.input") as f:
        return [
            f.strip().replace("(", "( ").replace(")", " )").split()
            for f in f.readlines()
        ]


OPERATORS = set(["+", "*"])


def parse(line):
    output = []
    ops = []
    print("***", line)
    for sym in line:
        if sym in OPERATORS:
            while ops and ops[-1] in OPERATORS:
                output.append(ops.pop())
            ops.append(sym)
        elif sym == "(":
            ops.append(sym)
        elif sym == ")":
            while ops[-1] != "(":
                output.append(ops.pop())
            ops.pop()
        else:
            output.append(int(sym))

        print(sym, output, ops)
    while ops:
        output.append(ops.pop())

    print("= ", output)
    return output


def eval_rpn(stack):
    print("eval", stack)
    sym = stack.pop()
    while stack[-1] in OPERATORS:
        stack.append(eval_rpn(stack))
    
    rhs = stack.pop()
    while stack[-1] in OPERATORS:
        stack.append(eval_rpn(stack))
    lhs = stack.pop()

    print(stack, sym, lhs, rhs)
    if sym == "+":
        return lhs + rhs
    else:
        return lhs * rhs


def main():
    res = [eval_rpn(parse(line)) for line in data()]
    print(res)
    print(sum(res))


main()
