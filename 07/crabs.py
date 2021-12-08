from statistics import median, mean


def crabs(input: str) -> None:
    with open(input) as f:
        crabs = [int(x) for x in f.readline().strip().split(',')]

    # Part 1
    target_pos = int(median(crabs))
    fuel = sum([abs(crab - target_pos) for crab in crabs])
    print(f"Aligning the crabs would cost {fuel} fuel")

    # Part 2
    target_pos = round(mean(crabs))
    nth = lambda n: int(n * (n + 1) / 2)  # Sum of N natural numbers
    fuel = sum([nth(abs(crab - target_pos)) for crab in crabs])
    print(f"Having understood crab engineering, it would cost {fuel} fuel")


if __name__ == "__main__":
    crabs("input")
