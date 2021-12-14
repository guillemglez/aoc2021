from typing import Dict


def polymer(input: str) -> None:
    rules: Dict[str, Dict[str, str]] = {}
    with open(input) as f:
        polymer = [p for p in f.readline().strip()]
        f.readline()  # empty line
        for line in f:  # rules
            rule = [c.strip() for c in line.split('->')]
            pair = rule[0]
            insert = rule[1]
            if pair[0] not in rules:
                rules[pair[0]] = {}
            rules[pair[0]][pair[1]] = insert

    for iteration in range(10):
        inserted = 0
        for pos in range(len(polymer) - 1):
            first = polymer[pos + inserted]
            second = polymer[pos + inserted + 1]
            if first in rules and second in rules[first]:
                polymer.insert(pos + inserted + 1, rules[first][second])
                inserted += 1

    occurrences = [polymer.count(p) for p in set(polymer)]
    print(
        f"Difference between most and least is {max(occurrences)-min(occurrences)}"
    )


if __name__ == "__main__":
    polymer("input")
