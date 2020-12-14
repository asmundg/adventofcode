import re

mask_re = re.compile(r"^mask = ([X01]+)$")
assign_re = re.compile(r"^mem\[(\d+)\] = (\d+)$")


def mask_out(number, mask):
    for i, char in enumerate(reversed(mask)):
        if char == "X":
            continue
        if char == "0":
            number &= ~(1 << i)
        else:
            number |= 1 << i
    return number


def main():
    mem = {}

    with open("input/14.input") as f:
        mask = "".join(["X" for _ in range(36)])
        for line in f.readlines():
            if mask_re.match(line):
                (mask,) = mask_re.match(line).groups()
                print(mask)
            else:
                address, number = assign_re.match(line).groups()
                mem[address] = mask_out(int(number), mask)
                print(address, number, mem)

    print(sum(mem.values()))


main()
