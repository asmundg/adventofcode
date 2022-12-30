"""Day 10: 
"""


def solve(start: str, iters: int) -> int:
    s = start
    for count in range(iters):
        new = ""
        current_char = None
        current_count = 0
        for c in s:
            if c != current_char:
                if current_char is not None:
                    new += f"{current_count}{current_char}"
                current_char = c
                current_count = 1
            else:
                current_count += 1
        new += f"{current_count}{current_char}"
        s = new
    return len(s)


print(solve("1", 5))
print(solve("1113222113", 40))
print(solve("1113222113", 50))
