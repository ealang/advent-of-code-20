from typing import List, Set, Optional, Tuple


def read_input(filename: str) -> List[int]:
    with open(filename) as fp:
        return list(map(int, fp.readlines()))


def make_circular_buffer(buf: List[int]):
    buf = buf[:]
    n = len(buf)
    i = 0

    def push(num: int) -> int:
        nonlocal i
        old_num = buf[i]
        buf[i] = num
        i = (i + 1) % n
        return old_num

    return push


def find_pair_sum(target_num: int, pool: Set[int]) -> Optional[Tuple[int, int]]:
    for num in pool:
        needed = target_num - num
        if needed != num and needed in pool:
            return num, needed

    return None


def part1_find_magic_number(nums: List[int]) -> Optional[int]:
    WINDOW_SIZE = 25

    window = set(nums[:WINDOW_SIZE])
    buf = make_circular_buffer(nums[:WINDOW_SIZE])

    for num in nums[WINDOW_SIZE:]:
        if find_pair_sum(num, window) is None:
            return num

        window.remove(buf(num))
        window.add(num)

    return None


def part2_find_encryption_weakness(magic_num: int, nums: List[int]) -> Optional[int]:
    i = 0
    cur_sum = 0

    for j in range(len(nums)):
        cur_sum += nums[j]
        while cur_sum >= magic_num and i <= j:
            if cur_sum == magic_num and i != j:
                window = nums[i: j + 1]
                return min(window) + max(window)

            cur_sum -= nums[i]
            i += 1

    return None


def main():
    nums = read_input("input.txt")
    magic_num = part1_find_magic_number(nums)
    assert magic_num is not None
    weakness = part2_find_encryption_weakness(magic_num, nums)

    print(magic_num)
    print(weakness)


main()
