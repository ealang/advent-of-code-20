import itertools

CELL_FLOOR = "."
CELL_EMPTY_SEAT = "L"
CELL_OCCUPIED_SEAT = "#"


def board_walk(x, y, dx, dy, width, height):
    x += dx
    y += dy
    while 0 <= x < width and 0 <= y < height:
        yield x, y
        x += dx
        y += dy


def count_visibly_occupied_seats_from(seats, x, y, max_dist=None):
    directions = [
        (1, 0),
        (1, 1),
        (0, 1),
        (-1, 1),
        (-1, 0),
        (-1, -1),
        (0, -1),
        (1, -1),
    ]
    height = len(seats)
    width = len(seats[0])

    num = 0
    for dx, dy in directions:
        for i, (xx, yy) in enumerate(board_walk(x, y, dx, dy, width, height)):
            if max_dist is not None and i + 1 > max_dist:
                break
            if seats[yy][xx] == CELL_EMPTY_SEAT:
                break
            if seats[yy][xx] == CELL_OCCUPIED_SEAT:
                num += 1
                break
    return num


def next_seat_state_adjacent(seats, x, y):
    """ Use part 1 adjacency rules to compute next state. """
    cell = seats[y][x]
    if cell == CELL_FLOOR:
        return CELL_FLOOR

    num = count_visibly_occupied_seats_from(seats, x, y, max_dist=1)
    if cell == CELL_OCCUPIED_SEAT and num >= 4:
        return CELL_EMPTY_SEAT
    if cell == CELL_EMPTY_SEAT and num == 0:
        return CELL_OCCUPIED_SEAT
    return cell


def next_seat_state_visible(seats, x, y):
    """ Use part 2 line of sight rules to compute next state. """
    cell = seats[y][x]
    if cell == CELL_FLOOR:
        return CELL_FLOOR

    num = count_visibly_occupied_seats_from(seats, x, y)
    if cell == CELL_OCCUPIED_SEAT and num >= 5:
        return CELL_EMPTY_SEAT
    if cell == CELL_EMPTY_SEAT and num == 0:
        return CELL_OCCUPIED_SEAT
    return cell


def next_seats_state(seats, next_seat_state):
    height = len(seats)
    width = len(seats[0])
    return [
        [
            next_seat_state(seats, x, y)
            for x in range(width)
        ]
        for y in range(height)
    ]


def strfmt_seats(seats):
    return '\n'.join(
        ''.join(row)
        for row in seats
    )


def count_occupied_seats(seats):
    return sum(
        1
        for row in seats
        for cell in row
        if cell == CELL_OCCUPIED_SEAT
    )


def run_to_completion(seats, next_seat_state) -> int:
    last = strfmt_seats(seats)
    while True:
        seats = next_seats_state(seats, next_seat_state)
        cur = strfmt_seats(seats)
        if cur == last:
            break
        last = cur

    return count_occupied_seats(seats)


def main():
    with open("input.txt") as fp:
        seats = [
            list(_.strip())
            for _ in fp.readlines()
        ]

    print(run_to_completion(seats, next_seat_state_adjacent))
    print(run_to_completion(seats, next_seat_state_visible))


main()
