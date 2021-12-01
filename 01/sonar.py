from typing import Optional, Tuple


def sonar(inputFile: str) -> None:
    increased: int = 0
    sums: int = 0

    with open(inputFile) as input:
        previous: Optional[int] = None
        window: Tuple[Optional[int], Optional[int],
                      Optional[int]] = (None, ) * 3

        for line in input:
            depth = int(line.strip())

            # Part one
            if previous is not None and depth > previous:
                increased += 1
            previous = depth

            # Part two
            # First pass
            if None in window:
                window = (depth if window[0] is None else window[0] + depth,
                          None if window[0] is None else
                          depth if window[1] is None else window[1] + depth,
                          None if window[1] is None else depth)
                continue

            # Subsequent passes
            popped = window[0]
            window = (window[1] + depth, window[2] + depth, depth)

            if window[0] > popped:
                sums += 1

    print(f"{increased} measurements are larger than the previous measurement")
    print(f"{sums} sums are larger than the previous sum")


if __name__ == "__main__":
    sonar('input')
