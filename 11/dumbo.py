from typing import List, Tuple
import numpy as np


class School:
    def __init__(self, input: List[str]) -> None:
        matrix: List[List[int]] = []
        for line in input:
            if len(line.strip()) == 0:
                break

            octopuses: List[int] = []
            for octopus in line.strip():
                octopuses.append(int(octopus))
            matrix.append(octopuses)

        self.grid = np.array(matrix)

    def simulate(self, steps: int) -> int:
        stepped = 0
        flashed = 0
        # Initially, we add one to all octopuses
        sum = np.ones(self.grid.shape, dtype=int)
        while (True):
            # Perform the additions
            self.grid += sum
            # Handle flashes
            sum, flashes = self.flash()
            # If no flashes happened, we can move to next step
            if flashes == 0:
                stepped += 1  # Step done
                # If completed all steps, return flashes done
                if stepped == steps:
                    return flashed
                # Start next step by adding one to all octopuses
                sum = np.ones(self.grid.shape, dtype=int)
            else:  # If flashes happened, keep the consequences of it (sum) and add the flashes to the counter
                flashed += flashes

    def flash(self) -> Tuple[np.ndarray, int]:
        flashed = self.grid > 9

        nextsum = np.zeros(self.grid.shape, dtype=int)
        # If none flashed, return 0
        if flashed.sum() == 0:
            return nextsum, 0

        # The ones which flashed go back to value zero
        self.grid[flashed] = 0
        # Handle consequences of flashes: neighbors +1
        maxr, maxc = self.grid.shape
        with np.nditer(flashed, flags=['multi_index'],
                       op_flags=['readonly']) as it:
            for flash in it:
                if flash:  # for each flashed
                    r, c = it.multi_index  # row, column
                    # Iterate neighbors
                    for i in range(-1, 2):
                        for j in range(-1, 2):
                            # Bound checking
                            if r + i in range(maxr) and c + j in range(maxc):
                                # If flashed in this step (value is 0), do not increase energy
                                if self.grid[r + i, c + j] != 0:
                                    # Add +1 to this neighboring octopus
                                    nextsum[r + i, c + j] += 1

        # Return next sum and amount of flashes to be handled in the next step
        return nextsum, flashed.sum()

    def __repr__(self) -> str:
        return str(self.grid)


def dumbo(input: str) -> None:
    with open(input) as f:
        school = School(f.readlines())
    steps = 100
    print(
        f"After {steps} steps there will be {school.simulate(steps)} flashes")


if __name__ == "__main__":
    dumbo("input")
