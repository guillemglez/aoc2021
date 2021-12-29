from typing import Final, Generator, List, NewType, Tuple, cast
from itertools import product, permutations

ScannerPos = NewType('ScannerPos', Tuple[int, int, int])
SCANNER_UNION_REQUIREMENT: Final = 12


def rotate(
        scanners: List[ScannerPos]) -> Generator[List[ScannerPos], None, None]:
    for px, py, pz in product([1, -1], repeat=3):
        for mx, my, mz in permutations([0, 1, 2]):
            # If det of the rotation matrix is -1, then this is not a real rotation
            rm = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
            rm[0][mx] = px
            rm[1][my] = py
            rm[2][mz] = pz
            # yapf: disable
            if (rm[0][0] * (rm[1][1] * rm[2][2] - rm[2][1] * rm[1][2])
               -rm[1][0] * (rm[0][1] * rm[2][2] - rm[2][1] * rm[0][2])
               +rm[2][0] * (rm[0][1] * rm[1][2] - rm[1][1] * rm[0][2])) == -1:
                continue
            # yapf: enable

            yield [
                ScannerPos((px * pos[mx], py * pos[my], pz * pos[mz]))
                for pos in scanners
            ]


def beacons(input: str) -> None:
    beacons: List[List[ScannerPos]] = []
    with open(input) as f:
        for line in f:
            line = line.strip()
            if not len(line):
                continue
            if line.startswith("---"):
                beacons.append([])
                continue
            xyz = [int(c) for c in line.split(',')]
            scanner = ScannerPos((xyz[0], xyz[1], xyz[2]))
            beacons[-1].append(scanner)

    map = beacons.pop()
    offsets = [(0, 0, 0)]
    while len(beacons):
        for i, beacon in enumerate(beacons):
            correlated = False
            for permuted in rotate(beacon):
                for seen in permuted:
                    for scanner in map[:-(SCANNER_UNION_REQUIREMENT - 1)]:
                        offset = cast(
                            ScannerPos,
                            tuple(b - a for a, b in zip(seen, scanner)))
                        corrected = [
                            cast(
                                ScannerPos,
                                tuple(s + off
                                      for s, off in zip(scanner, offset)))
                            for scanner in permuted
                        ]

                        equal = [scanner in map for scanner in corrected]
                        if sum(equal) >= SCANNER_UNION_REQUIREMENT:
                            for scanner in corrected:
                                if scanner not in map:
                                    map.append(scanner)
                            offsets.append(offset)
                            correlated = True
                            break

                    if correlated:
                        break

                if correlated:
                    break

            if correlated:
                beacons.pop(i)
                break

        if not correlated:
            raise Exception("Could not correlate!")

    print(f"There are {len(map)} beacons in the sea")

    # Part 2
    distances = []
    for xof, yof, zof in offsets:
        for xoff, yoff, zoff in offsets:
            distances.append(
                sum((abs(xof - xoff), abs(yof - yoff), abs(zof - zoff))))
    print(f"The largest Manhattan distance is {max(distances)}")


if __name__ == "__main__":
    beacons("input")
