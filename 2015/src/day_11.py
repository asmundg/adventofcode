"""Day 11: 
"""

import re


def increment(s: str) -> str:
    if not s:
        return "a"

    n = ord(s[-1]) + 1
    candidate = s[:-1] + chr(n) if n <= 122 else increment(s[:-1]) + "a"
    for illegal in ("i", "l", "o"):
        if illegal in candidate:
            idx = candidate.index(illegal)
            return (
                candidate[:idx]
                + chr(ord(illegal) + 1)
                + "a" * (len(candidate) - 1 - idx)
            )
    return candidate


def valid(s: str) -> bool:
    found = False
    for n in range(len(s) - 2):
        if s[n + 1] == chr(ord(s[n]) + 1) and s[n + 2] == chr(ord(s[n]) + 2):
            found = True
            break
    if not found:
        return False

    if "i" in s or "o" in s or "l" in s:
        return False

    return re.search(r"([a-z])\1.*([a-z])\2", s) is not None


def solve(s: str) -> str:
    while True:
        s = increment(s)
        if valid(s):
            return s


assert increment("a") == "b"
assert increment("az") == "ba"
assert increment("zz") == "aaa"

assert not valid("hijklmmn")
assert not valid("abbceffg")
assert not valid("abbcegjk")

assert solve("abcdefgh") == "abcdffaa"
assert solve("ghijklmn") == "ghjaabcc"

print(solve("hepxcrrq"))
print(solve(solve("hepxcrrq")))
