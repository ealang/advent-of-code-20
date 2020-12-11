import collections
import itertools
from typing import List, Iterable


def memoized(f):
    cache = {}
    def memoized_f(value):
        if value not in cache:
            cache[value] = f(value)
        return cache[value]
    return memoized_f


@memoized
def fib_3(n: int) -> int:
    if n <= 0:
        return 0
    if n <= 2:
        return 1
    return fib_3(n - 1) + fib_3(n - 2) + fib_3(n - 3)


def compute_deltas(items: List[int], initial: int) -> Iterable[int]:
    for item in items:
        yield item - initial
        initial = item


def main():
    with open("input.txt") as fp:
        adapters = list(sorted(map(int, fp.readlines())))

    deltas = list(compute_deltas(adapters, initial=0))

    # part 1
    counts = collections.Counter(deltas)
    counts[3] += 1  # include device's adapter in counts
    print(counts[1] * counts[3])

    # part 2
    num_combos = 1
    for delta, items in itertools.groupby(deltas):
        if delta == 1:
            n = 1 + sum(1 for _ in items)
            num_combos *= fib_3(n)

    print(num_combos)


main()
