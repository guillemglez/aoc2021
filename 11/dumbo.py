from typing import Final, List, Tuple
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

        self.constgrid: Final = np.array(matrix)
        self.grid = self.constgrid.copy()

    def simulate(self, steps: int | None = None) -> int:
        """
        Returns number of flashes per given number of steps (part 1) 
        OR 
        number of steps until all flash at the same time (part 2) if arg steps is not provided
        """
        stepped = 0
        flashed = 0
        self.grid = self.constgrid.copy()
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
                if steps is not None and stepped == steps:
                    return flashed
                # Start next step by adding one to all octopuses
                sum = np.ones(self.grid.shape, dtype=int)

                # If resolved part 2
                if steps is None and self.grid.sum() == 0:
                    return stepped

            else:  # Otherwise, add the flashes to the counter and go on
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

    school = School(open(input).readlines())

    steps: Final = 100
    print(
        f"After {steps} steps there will be {school.simulate(steps)} flashes")
    print(
        f"They will all flash at the same time after {school.simulate()} steps"
    )


if __name__ == "__main__":
    dumbo("input")
