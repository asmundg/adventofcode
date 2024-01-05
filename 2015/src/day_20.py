"""Day 20: Infinite Elves and Infinite Houses

More math. Numbers of elves delivering presents to any house are the
divisors of the house number. Brute force-calculating the divisors is
too slow, so we do some trickery with prime factorization
instead. Fast divisor algorithm shamelessly stolen from the internet.

"""

import collections
import itertools
from typing import Generator


def prime_factors(n: int) -> Generator[int, None, None]:
    i = 2
    while i**2 <= n:
        if n % i == 0:
            yield i
            n //= i
        else:
            i += 1

    if n > 1:
        yield n


def prod(iterable):
    result = 1
    for i in iterable:
        result *= i
    return result


def divisors(n):
    powers = [
        [factor**i for i in range(count + 1)]
        for factor, count in collections.Counter(prime_factors(n)).items()
    ]

    for prime_power_combo in itertools.product(*powers):
        yield prod(prime_power_combo)


def part1(target: int) -> int:
    c = 0
    while True:
        c += 1
        gifts = sum(10 * n for n in divisors(c))
        if gifts > target:
            return c


def part2(target: int) -> int:
    c = 0
    while True:
        c += 1
        gifts = sum(11 * n for n in divisors(c) if c <= 50 * n)
        if gifts > target:
            return c


if __name__ == "__main__":
    print(part1(33100000))
    print(part2(33100000))
