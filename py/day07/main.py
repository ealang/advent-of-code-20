import re
from typing import Dict, List, Tuple, NamedTuple


class BagDependency(NamedTuple):
    color: str
    quantity: int


def parse_rule_line(line: str) -> Tuple[str, List[BagDependency]]:
    def clean_child(child: str) -> BagDependency:
        match = re.match(r"(\d+) (.*?) bags?", child)
        assert match, child
        quantity_str, color = match.groups()
        return BagDependency(color, int(quantity_str))

    match = re.match(r"(.*?) bags contain (.*?)\.", line)
    assert match, line
    parent, children_line = match.groups()

    if children_line == "no other bags":
        return (parent, [])

    children = map(clean_child, children_line.split(", "))
    return (parent, list(children))


def load_bag_dependency_tree(filename: str) -> Dict[str, List[BagDependency]]:
    """ Bag color to dependencies. """
    with open(filename) as fp:
        return dict(
            parse_rule_line(line)
            for line in fp.readlines()
        )


def count_containable(target_color: str, tree: Dict[str, List[BagDependency]]) -> int:
    """ Num bag colors that can contain this color. """
    cache: Dict[str, bool] = dict()
    count = 0

    def visit(color) -> bool:
        if color in cache:
            return cache[color]

        can_reach = (color == target_color) or any(
            visit(child.color)
            for child in tree[color]
        )
        cache[color] = can_reach
        if can_reach:
            nonlocal count
            count += 1
        return can_reach

    for color in tree:
        visit(color)

    return count - 1


def recursive_bag_count(color: str, tree: Dict[str, List[BagDependency]]) -> int:
    """ Number of bags contained within this bag. """
    return sum(
        child.quantity * (1 + recursive_bag_count(child.color, tree))
        for child in tree[color]
    )


tree = load_bag_dependency_tree("input.txt")
print(count_containable("shiny gold", tree))
print(recursive_bag_count("shiny gold", tree))
