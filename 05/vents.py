from typing import List, Tuple
import numpy as np


class Point:
    def __init__(self, x: str, y: str) -> None:
        self.x = int(x)
        self.y = int(y)

    # for debugging
    def __repr__(self) -> str:
        return f"{self.x},{self.y}"


def parse(input: str) -> List[Tuple[Point, Point]]:
    coords: List[Tuple[Point, Point]] = []
    with open(input) as f:
        for line in f:
            pairs = line.strip().split("->")
            first_raw = pairs[0].strip().split(",")
            second_raw = pairs[1].strip().split(",")
            first = Point(first_raw[0], first_raw[1])
            second = Point(second_raw[0], second_raw[1])
            coords.append((first, second))
    return coords


def one(coords: List[Tuple[Point, Point]]) -> int:
    xmax, ymax = 0, 0
    for coord in coords:
        xmax = max(xmax, coord[0].x, coord[1].x)
        ymax = max(ymax, coord[0].y, coord[1].y)

    diagram = np.zeros((ymax + 1, xmax + 1), dtype=int)
    for first, second in coords:
        # Only vertical or horizontal
        if not ((first.x == second.x) or (first.y == second.y)):
            continue

        x1 = min(first.x, second.x)
        x2 = max(first.x, second.x) + 1
        y1 = min(first.y, second.y)
        y2 = max(first.y, second.y) + 1
        diagram[y1:y2, x1:x2] += 1

    return np.count_nonzero(diagram > 1)


def vents(input: str) -> None:
    print(f"Lines overlap at {one(parse(input))} points")


if __name__ == "__main__":
    vents("input")
