from typing import List


def parse_group(group_text: str) -> List[str]:
    return [
        line.strip() for line in group_text.splitlines()
    ]


with open("input.txt") as fp:
    groups = list(map(parse_group, fp.read().split("\n\n")))


def unique_response_count(group: List[str]) -> int:
    return set(''.join(group))


def union_response_count(group: List[str]) -> int:
    value = set(group[0])
    for response in group[1:]:
        value = value.intersection(set(response))
    return value


print('Part 1', sum(
    len(unique_response_count(group))
    for group in groups
))

print('Part 2', sum(
    len(union_response_count(group))
    for group in groups
))
