from typing import List
import numpy as np


def smoke(input: str) -> None:
    matrix: List[List[int]] = []
    with open(input) as f:
        for line in f:
            matrix.append([int(n) for n in line.strip()])

    heightmap = np.array(matrix)
    risk = 0
    with np.nditer(heightmap, flags=['multi_index'],
                   op_flags=['readonly']) as it:
        for height in it:
            neighbors: List[int] = []

            tryAppend = lambda r, c: neighbors.append(heightmap[r, c]) if (
                (r in range(heightmap.shape[0])) and
                (c in range(heightmap.shape[1]))) else None

            r, c = it.multi_index
            for i in (-1, 1):
                tryAppend(r + i, c)
            for j in (-1, 1):
                tryAppend(r, c + j)

            if all([neighbor > height for neighbor in neighbors]):
                risk += height + 1

    print(f"The sum of the risk levels is {risk}")


if __name__ == "__main__":
    smoke("input")
