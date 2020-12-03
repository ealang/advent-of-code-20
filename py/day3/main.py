import functools

def load_terrain():
    with open("input.txt") as fp:
        return map(str.strip, fp.readlines())

terrain = load_terrain()

height = len(terrain)
width = len(terrain[0])

TREE = "#"

def tree_count(dx, dy):
    x = 0
    y = 0
    count = 0
    while y < height:
        if terrain[y][x % width] == TREE:
            count += 1
        x += dx
        y += dy

    return count

print(tree_count(dx=3, dy=1))

print(
    functools.reduce(
        lambda x, y: x * y,
        (
            tree_count(dx, dy)
            for dx, dy in
            [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
        ),
    )
)

