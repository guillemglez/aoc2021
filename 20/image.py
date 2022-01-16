import os
from typing import Final, List
from copy import deepcopy


class Trench:
    algorithm: List[bool] = []

    def __init__(self) -> None:
        self.image: List[List[bool]] = []
        self.extendvalue = False

    def append(self, line: List[bool]) -> None:
        self.image.append(line)

    def lit(self) -> int:
        return sum([sum(line) for line in self.image])

    def apply(self, times: int) -> int:
        for _ in range(times):
            self.iterate()
        return self.lit()

    def iterate(self) -> None:
        self.extend()
        initial = deepcopy(self.image)
        for r, row in enumerate(initial):
            for c in range(len(row)):
                number = 0
                neighborcount = 8
                for ro in (-1, 0, 1):
                    for co in (-1, 0, 1):
                        if ((r + ro) not in range(len(self.image))) or (
                            (c + co) not in range(len(row))):
                            value = self.extendvalue
                        else:
                            value = initial[(r + ro)][(c + co)]
                        # if r == 3 and c == 3:
                        #     print(f"r+ro={r}+{ro}={r+ro}, c+co={c}+{co}={c+co} => {value}")
                        number += value << neighborcount
                        neighborcount -= 1
                # if r == 3 and c == 3:
                #     print(number)
                self.image[r][c] = Trench.algorithm[number]
        self.extendvalue = Trench.algorithm[-1 if self.extendvalue else 0]

    def extend(self) -> None:
        for row in self.image:
            row.insert(0, self.extendvalue)
            row.append(self.extendvalue)

        self.image.insert(0, [self.extendvalue] * len(self.image[0]))
        self.image.append([self.extendvalue] * len(self.image[0]))

    def __repr__(self) -> str:
        repr = ""
        for row in self.image:
            repr += ''.join(["#" if v else "." for v in row])
            repr += os.linesep
        return repr


def image(input: str) -> None:
    with open(input) as f:
        # read image enhancement algorithm
        Trench.algorithm = ["#" == x for x in f.readline().strip()]
        f.readline()  # must be empty

        # read image
        trench = Trench()
        for line in f:
            if line.startswith(os.linesep):
                break
            trench.append(["#" == x for x in line.strip()])

        print(f"There are {trench.apply(2)} pixels lit")


if __name__ == "__main__":
    image("input")
