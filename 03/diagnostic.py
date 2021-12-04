from typing import List
import enum


class Rating(enum.Enum):
    OXIGEN_GENERATOR_RATING = enum.auto()
    CO2_SCRUBBER_RATING = enum.auto()


def oxigen_generator_rating(report: List[str]) -> int:
    return find_rating(report.copy(), Rating.OXIGEN_GENERATOR_RATING, 0)


def co2_scrubber_rating(report: List[str]) -> int:
    return find_rating(report.copy(), Rating.CO2_SCRUBBER_RATING, 0)


def find_rating(report: List[str], rating: Rating, i: int) -> int:

    if (len(report) == 1):
        return int(report[0], 2)

    votes = 0
    for number in report:
        if (number[i] == "1"):
            votes += 1

    if rating is Rating.OXIGEN_GENERATOR_RATING:
        keep = "1" if votes >= len(report) / 2 else "0"
    else:
        keep = "0" if votes >= len(report) / 2 else "1"

    remove: List[int] = []
    for n, number in enumerate(report):
        if number[i] != keep:
            remove.append(n)

    for n in reversed(remove):
        report.pop(n)

    return find_rating(report, rating, i + 1)


def diagnostic(input: str) -> None:
    votes: List[int] = []
    number_length = 0
    diagnostic_length = 0
    report: List[str] = []
    with open(input) as f:
        for line in f:
            # First pass
            if not len(votes):
                number_length = len(line.strip())
                votes = [0] * number_length

            diagnostic_length += 1
            report.append(line.strip())

            for b in range(number_length - 1):
                if line[b] == "1":
                    votes[number_length - 1 - b] += 1

    gamma = 0
    epsilon = 0
    for b, v in enumerate(votes):
        if v > diagnostic_length // 2:
            gamma |= (1 << b)
        else:
            epsilon |= (1 << b)

    print(f"The power consumption is {gamma*epsilon}")
    print(
        f"The life support rating is {co2_scrubber_rating(report) * oxigen_generator_rating(report)}"
    )


if __name__ == "__main__":
    diagnostic('input')
