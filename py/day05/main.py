from typing import Tuple, List


SEATS_NROWS = 128
SEATS_NCOLS = 8


def decode_seat_coord(bsp: str) -> Tuple[int, int]:
    def take_mid(range_val):
        return sum(range_val) // 2

    def take_lower(range_val):
        lo, _ = range_val
        return (lo, take_mid(range_val))

    def take_upper(range_val):
        _, hi = range_val
        return (take_mid(range_val) + 1, hi)

    row_range = (0, SEATS_NROWS - 1)
    col_range = (0, SEATS_NCOLS - 1)
    for char in bsp:
        if char == "F":
            row_range = take_lower(row_range)
        elif char == "B":
            row_range = take_upper(row_range)
        elif char == "L":
            col_range = take_lower(col_range)
        else:
            col_range = take_upper(col_range)

    return take_mid(row_range), take_mid(col_range)


def seat_id(coordinates: Tuple[int, int]) -> int:
    row, col = coordinates
    return row * 8 + col


def find_empty_seat(start_id: int, end_id: int, sorted_seat_ids: List[int]) -> int:
    for i in range(start_id, end_id + 1):
        if i not in sorted_seat_ids:
            return i
    return -1


with open("input.txt") as fp:
    seat_coords = list(map(decode_seat_coord, fp.readlines()))

sorted_seat_ids = list(sorted(map(seat_id, seat_coords)))

print("Max seat id:", sorted_seat_ids[-1])
print(
    "My seat id:",
    find_empty_seat(
        start_id=seat_id((2, 0)),
        end_id=seat_id((SEATS_NROWS - 2, 0)),
        sorted_seat_ids=sorted_seat_ids,
    ),
)
