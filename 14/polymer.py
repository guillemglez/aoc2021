from typing import Dict, Final, List


def polymer(input: str) -> None:
    rules: Dict[str, str] = {}
    with open(input) as f:
        pairs = [p for p in f.readline().strip()]
        pairs = [pairs[i] + pairs[i + 1] for i in range(len(pairs) - 1)]
        f.readline()  # empty line
        for line in f:  # rules
            rule = [c.strip() for c in line.split('->')]
            pair = rule[0]
            insert = rule[1]
            rules[pair] = insert

    # keep the last character since it will need to be counted apart
    last: Final = pairs[-1][-1]
    # keep a dictionary of present pairs, which will be mutated following the collected rules
    polymer = {pair: pairs.count(pair) for pair in rules.keys()}

    for iteration in range(1, 40 + 1):
        after = polymer.copy()
        for pair, insert in rules.items():
            if pair not in polymer.keys() or polymer[pair] == 0:
                continue
            becomes = pair[0] + insert
            adds = insert + pair[1]

            if becomes not in after.keys():
                after[becomes] = polymer[pair]
            else:
                after[becomes] += polymer[pair]

            if adds not in after.keys():
                after[adds] = polymer[pair]
            else:
                after[adds] += polymer[pair]

            after[pair] -= polymer[pair]
        polymer = after.copy()

        if iteration == 10 or iteration == 40:
            # Take all unique characters in polymer and add all the counts in all pairs in which they appear in first
            # position, +1 if it was the character in last position in the initial polymer
            occurrences = [
                sum([count
                     for pair, count in polymer.items() if pair[0] == p]) +
                (1 if p == last else 0) for p in set(''.join(polymer.keys()))
            ]
            print(
                f"Difference between most and least is {max(occurrences)-min(occurrences)} at {iteration} iterations"
            )


if __name__ == "__main__":
    polymer("input")
