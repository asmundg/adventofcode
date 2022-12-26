"""Day 4: 
"""

import hashlib
import itertools


def solve(secret: str, prefix: int = 5) -> int:
    for i in itertools.count(start=1):
        if (
            hashlib.md5((secret + str(i)).encode("ascii"))
            .hexdigest()
            .startswith("0" * prefix)
        ):
            return i

    raise Exception("Should never get here")


assert solve("abcdef") == 609043
print(solve("iwrupvqb"))
print(solve("iwrupvqb", 6))
