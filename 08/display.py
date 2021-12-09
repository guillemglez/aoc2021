from typing import Final, List, Tuple


class Display:
    segments: Final = {
        0: [True, True, True, True, True, True, False],
        1: [False, True, True, False, False, False, False],
        2: [True, True, False, True, True, False, True],
        3: [True, True, True, True, False, False, True],
        4: [False, True, True, False, False, True, True],
        5: [True, False, True, True, False, True, True],
        6: [True, False, True, True, True, True, True],
        7: [True, True, True, False, False, False, False],
        8: [True, True, True, True, True, True, True],
        9: [True, True, True, True, False, True, True]
    }

    def __init__(self, patterns: List[str]) -> None:
        self.patterns = patterns
        self.map = ['abcdefg'] * 7
        self.resolve()

    @staticmethod
    def numOfSegments(number: int) -> int:
        if number not in Display.segments.keys():
            raise Exception(f"Number {number}?")

        return len([d for d in Display.segments[number] if d])

    @staticmethod
    def isUnique(pattern: str) -> bool:
        # unique numbers are 1, 4, 7 and 8
        for n in (1, 4, 7, 8):
            if len(pattern) == Display.numOfSegments(n):
                return True
        return False

    @staticmethod
    def uniqueNumber(pattern: str) -> int:
        if not Display.isUnique(pattern):
            raise Exception("Not unique!")

        for n in Display.segments.keys():
            if Display.numOfSegments(n) == len(pattern):
                return n

        return -1

    def resolve(self) -> None:
        # First pass: unique patterns
        for pattern in self.patterns:
            if not Display.isUnique(pattern):
                continue

            # We will be done once all the mappings are reduced to two possibilities
            if all([len(m) == 2 for m in self.map]):
                break

            number = Display.uniqueNumber(pattern)
            for segment, high in enumerate(Display.segments[number]):
                # If high, then the provided wires are the only possibilities for this segment
                if high:
                    self.map[segment] = ''.join(
                        [s for s in pattern if s in self.map[segment]])
                # If low, then the provided wires are not part of this segment
                else:  # low
                    for m in pattern:
                        self.map[segment] = self.map[segment].replace(m, '')

        # Will be resolved when all wires are mapped to a single segment
        resolved: Final = lambda: all([len(m) == 1 for m in self.map])

        # Second pass: use 9, 6 and 0 to complete the mapping. These numbers have all segments high except one
        for pattern in self.patterns:
            if len(pattern) == 6:  # 9 6 or 0 (all segments but one are high)
                missing = [d for d in 'abcdefg'
                           if d not in pattern][0]  # Take the one missing
                for s in (1, 4, 6):  # Indexes of segments which might be low
                    if missing in self.map[s]:
                        # If it is a possibility in this segment, then we may conclude this is the solution for this
                        # segment. Assign it and remove this wire from all other segments.
                        for ss, m in enumerate(self.map):
                            self.map[ss] = m.replace(missing, '')
                        self.map[s] = missing

            if resolved():
                break

        if not resolved():
            raise Exception(f"Not resolved")

    def decode(self, given_output: List[str]) -> int:
        if len(given_output) != 4:
            raise Exception("Must be 4")

        decoded = 0
        for i, pattern in enumerate(given_output):
            output = [False] * 7
            for d in pattern:
                output[self.map.index(d)] = True

            for n, code in Display.segments.items():
                if code == output:
                    decoded += n * 10**(3 - i)

        return decoded


def display(input: str) -> None:
    notes: List[Tuple[List[str], List[str]]] = []
    with open(input) as f:
        for line in f:
            patterns = line.split('|')[0].strip().split()
            output = line.split('|')[1].strip().split()
            notes.append((patterns, output))

    unique_count = 0
    values_sum = 0
    for patterns, output in notes:
        for digit in output:
            if Display.isUnique(digit):
                unique_count += 1
        values_sum += Display(patterns).decode(output)

    print(f"1, 4, 7 or 8 appear {unique_count} times")
    print(f"Adding up all of the output values gives {values_sum}")


if __name__ == "__main__":
    display("input")
