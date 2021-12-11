from typing import Final, List, Tuple


class SyntaxError:
    CHUNK_CHARS = {"(": ")", "[": "]", "{": "}", "<": ">"}
    CHUNK_POINTS = {")": 3, "]": 57, "}": 1197, ">": 25137}

    def __init__(self, line: str) -> None:
        self.line = line.strip()

    def syntax_error_score(self) -> int:
        chunks: List[str] = []
        for c in self.line:
            if c in SyntaxError.CHUNK_CHARS.keys():  # if opener
                chunks.append(c)
            else:  # if closer
                if SyntaxError.CHUNK_CHARS[chunks.pop()] != c:
                    return SyntaxError.CHUNK_POINTS[c]
        return 0


def syntax(input: str) -> None:
    score = 0
    with open(input) as f:
        for line in f:
            score += SyntaxError(line).syntax_error_score()

    print(f"The syntax error score is {score}")


if __name__ == "__main__":
    syntax("input")
