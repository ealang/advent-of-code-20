import re

def parse(line):
    return re.match(r"(\d+)-(\d+) (\w): (\w+)", line).groups()

def count_char(s, c):
    return sum(1 for _ in s if _ == c)

def sled_policy(entry):
    minc, maxc, c, password = entry
    return int(minc) <= count_char(password, c) <= int(maxc)

def toboggan_policy(entry):
    pos1, pos2, c, password = entry
    return (password[int(pos1) - 1] == c) ^ (password[int(pos2) - 1] == c)

with open("input.txt") as fp:
    entries = list(map(parse, fp.readlines()))

def count_valid(entries, policy):
    return sum(1 for entry in entries if policy(entry))

print(count_valid(entries, sled_policy))
print(count_valid(entries, toboggan_policy))
