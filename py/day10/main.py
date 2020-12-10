from collections import defaultdict
from typing import Dict, List


def memoized(f):
    cache = {}
    def memoized_f(value):
        if value not in cache:
            cache[value] = f(value)
        return cache[value]
    return memoized_f


def part1_count_deltas(adapters: List[int]) -> int:
    cur_jolts = 0
    deltas: Dict[int, int] = defaultdict(int)
    for adapter in adapters:
        delta = adapter - cur_jolts
        deltas[delta] += 1
        cur_jolts = adapter

    deltas[3] +=1  # include device adapter

    return deltas[1] * deltas[3]


def part2_count_permutations(adapters: List[int]) -> int:
    device_jolts = adapters[-1] + 3

    available_jolts = set(adapters)
    available_jolts.add(0)
    available_jolts.add(device_jolts)

    @memoized
    def count_ways(t):
        if t not in available_jolts:
            return 0

        return max(
            1,
            count_ways(t - 1) + count_ways(t - 2) + count_ways(t - 3),
        )

    return count_ways(device_jolts)


def main():
    with open("input.txt") as fp:
        adapters = list(sorted(map(int, fp.readlines())))

    print(part1_count_deltas(adapters))
    print(part2_count_permutations(adapters))


main()
