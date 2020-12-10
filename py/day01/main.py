def part1(nums, target):
    for num in nums:
        needed = target - num
        if needed in nums:
            return num * needed

def part2(nums, target):
    for a in nums:
        for b in nums:
            needed = target - a - b
            if needed in nums:
                return a * b * needed

with open("input.txt") as fp:
    nums = set(map(int, fp.readlines()))

target = 2020

print(part1(nums, target))
print(part2(nums, target))
