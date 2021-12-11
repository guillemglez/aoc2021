from typing import List, Tuple
import numpy as np


def get_neighbors(index: Tuple[int, int],
                  shape: Tuple[int, ...]) -> List[Tuple[int, int]]:
    neighbors: List[Tuple[int, int]] = []
    r, c = index
    sr, sc = shape
    for i in (-1, 1):
        if (r + i) in range(sr):
            neighbors.append((r + i, c))
    for j in (-1, 1):
        if (c + j) in range(sc):
            neighbors.append((r, c + j))
    return neighbors


def smoke(input: str) -> None:
    matrix: List[List[int]] = []
    with open(input) as f:
        for line in f:
            matrix.append([int(n) for n in line.strip()])

    heightmap = np.array(matrix)
    risk = 0
    basins: List[int] = []
    with np.nditer(heightmap, flags=['multi_index'],
                   op_flags=['readonly']) as it:
        for height in it:
            neighbors = get_neighbors(it.multi_index, heightmap.shape)

            lowvalues: List[int] = []
            for neighbor in neighbors:
                lowvalues.append(heightmap[neighbor])

            # If a low point
            if all([neighbor > height for neighbor in lowvalues]):
                # Part 1
                risk += height + 1

                # Part 2
                basin = [it.multi_index]
                previous = -1
                while previous != len(basin):
                    previous = len(basin)
                    for index in basin:
                        for neighbor in get_neighbors(index, heightmap.shape):
                            if neighbor not in basin and heightmap[
                                    neighbor] != 9:
                                basin.append(neighbor)
                basins.append(len(basin))

    # Calculate part 2
    sizemult = 1
    for i in range(3):
        sizemult *= basins.pop(basins.index(max(basins)))

    print(f"The sum of the risk levels is {risk}")
    print(f"Multiplying the three biggest basins gives {sizemult}")


if __name__ == "__main__":
    smoke("input")
