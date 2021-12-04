from typing import List


def diagnostic(input: str) -> None:
    votes: List[int] = []
    number_length = 0
    diagnostic_length = 0
    with open(input) as f:
        for line in f:
            # First pass
            if not len(votes):
                number_length = len(line.strip())
                votes = [0] * number_length

            diagnostic_length += 1
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


if __name__ == "__main__":
    diagnostic('input')
