from typing import List, Tuple


def display(input: str) -> None:
    notes: List[Tuple[List[str], List[str]]] = []
    with open(input) as f:
        for line in f:
            patterns = line.split('|')[0].strip().split()
            output = line.split('|')[1].strip().split()
            notes.append((patterns, output))

    count = 0
    for patterns, output in notes:
        for segments in output:
            if len(segments) in [2, 4, 3, 7]:
                count += 1

    print(f"1, 4, 7 or 8 appear {count} times")


if __name__ == "__main__":
    display("input")
