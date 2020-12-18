def data():
    with open("input/18.input") as f:
        return [
            f.strip().replace("(", "( ").replace(")", " )").split()
            for f in f.readlines()
        ]


# The order of the operators indicate precedence, later in the array
# is higher.
def parse(line, precedence):
    operators = precedence.keys()
    output = []
    ops = []
    print("parsing", line)
    for sym in line:
        if sym in operators:
            while ops and ops[-1] in operators and precedence[ops[-1]] >= precedence[sym]:
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

    print("=", output)
    return output


def eval_rpn(stack, ops):
    print("eval", stack)
    sym = stack.pop()
    while stack[-1] in ops:
        stack.append(eval_rpn(stack, ops))
    
    rhs = stack.pop()
    while stack[-1] in ops:
        stack.append(eval_rpn(stack, ops))
    lhs = stack.pop()

    print("post eval", stack, sym, lhs, rhs)
    if sym == "+":
        return lhs + rhs
    else:
        return lhs * rhs


def main():
    ops = ["+", "*"]
    part1_res = [eval_rpn(parse(line, {"+": 0, "*": 0}), ops) for line in data()]
    print(part1_res)
    
    part2_res = [eval_rpn(parse(line, {"+": 1, "*": 0}), ops) for line in data()]
    print(part2_res)

    print("part1:", sum(part1_res))
    print("part2:", sum(part2_res))


main()
