def sonar(inputFile: str) -> None:
    increased: int = 0

    with open(inputFile) as input:
        previous: int = None

        for line in input:
            depth = int(line.strip())

            if (previous is None):
                previous = depth
                continue

            if (depth > previous):
                increased += 1

            previous = depth

    print(
        f"{increased} measurements are larger than the prevuious measurement")


if __name__ == "__main__":
    sonar('input')
