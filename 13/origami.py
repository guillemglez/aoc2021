from typing import List, Tuple
import os
import numpy as np


def origami(input: str) -> None:
    dots: List[Tuple[int, int]] = []
    folds: List[Tuple[str, int]] = []
    rmax, cmax = 0, 0
    with open(input) as f:
        for line in f:
            if line == os.linesep:
                break
            coordinates = [int(c) for c in line.strip().split(',')]
            dots.append((coordinates[1], coordinates[0]))
            rmax = max(rmax, coordinates[1])
            cmax = max(cmax, coordinates[0])
        for line in f:
            fold = line.strip().split()[-1].split('=')
            axis = fold[0]
            value = int(fold[1])
            folds.append((axis, value))

    paper = np.zeros((rmax + 1, cmax + 1), dtype=bool)
    for dot in dots:
        paper[dot] = True

    for axis, value in folds:
        if axis == 'y':
            up = paper[:value, ...]
            down = paper[1 + value:, ...]
            down = np.flipud(down)

            if up.size > down.size:
                extracols = np.zeros(
                    (up.shape[0] - down.shape[0], paper.shape[1]),
                    dtype=paper.dtype)
                paper = up + np.r_[extracols, down]
            elif up.size < down.size:
                extracols = np.zeros(
                    (down.shape[0] - up.shape[0], paper.shape[1]),
                    dtype=paper.dtype)
                paper = np.r_[up, extracols] + down
            elif up.size == down.size:
                paper = up + down

        if axis == 'x':
            left = paper[..., :value]
            right = paper[..., 1 + value:]
            right = np.fliplr(right)

            if left.size > right.size:
                extracols = np.zeros(
                    (paper.shape[0], left.shape[1] - right.shape[1]),
                    dtype=paper.dtype)
                paper = left + np.c_[extracols, right]
            elif left.size < right.size:
                extracols = np.zeros(
                    (paper.shape[0], right.shape[1] - left.shape[1]),
                    dtype=paper.dtype)
                paper = np.c_[left, extracols] + right
            elif left.size == right.size:
                paper = left + right
        break

    print(f"After the first fold, {paper.sum()} dots are visible")


if __name__ == "__main__":
    origami("input")
