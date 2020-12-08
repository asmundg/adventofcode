import re

instruction_re = re.compile(r"^(nop|acc|jmp) ((?:\+|\-)\d+)$")

instructions = []

with open("input/08.input") as f:
    for line in f.readlines():
        instruction, change = instruction_re.match(line).groups()
        instructions.append((instruction, change))

def nop(ip, acc, arg):
    return (ip + 1, acc)

def acc(ip, acc, arg):
    return (ip + 1, acc + arg)

def jmp(ip, acc, arg):
    return (ip + arg, acc)

ops = {"nop": nop,
       "acc": acc,
       "jmp": jmp}

acc = 0
ip = 0
visited = set([0])

while True:
    instruction, arg = instructions[ip]
    print(ip, acc, instruction, arg)
    ip, acc = ops[instruction](ip, acc, int(arg))
    if ip in visited:
        break
    else:
        visited.add(ip)

print(acc)
