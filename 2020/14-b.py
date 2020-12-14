import re

mask_re = re.compile(r"^mask = ([X01]+)$")
assign_re = re.compile(r"^mem\[(\d+)\] = (\d+)$")


def mask_out(number, mask, pos):
    if pos >= len(mask):
        return [number]

    char = mask[len(mask) - 1 - pos]
    if char == "1":
        return mask_out(number | (1 << pos), mask, pos + 1)
    if char == "0":
        return mask_out(number, mask, pos + 1)

    return mask_out(number | (1 << pos), mask, pos + 1) + mask_out(
        number & ~(1 << pos), mask, pos + 1
    )


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
                for masked_address in mask_out(int(address), mask, 0):
                    print(bin(int(address)), bin(masked_address), number)
                    mem[masked_address] = int(number)

    print(sum(mem.values()))


main()
