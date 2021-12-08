from statistics import median


def crabs(input: str) -> None:
    with open(input) as f:
        crabs = [int(x) for x in f.readline().strip().split(',')]

    target_pos = int(median(crabs))
    fuel = sum([abs(crab - target_pos) for crab in crabs])

    print(f"Aligning the crabs would cost {fuel} fuel")


if __name__ == "__main__":
    crabs("input")
