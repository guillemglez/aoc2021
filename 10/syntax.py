from typing import Final, List


class SyntaxError:
    CHUNK_CHARS: Final = {"(": ")", "[": "]", "{": "}", "<": ">"}
    CHUNK_ERROR_POINTS: Final = {")": 3, "]": 57, "}": 1197, ">": 25137}
    CHUNK_AUTOCOMPLETE_POINTS: Final = {")": 1, "]": 2, "}": 3, ">": 4}

    def __init__(self, line: str) -> None:
        self.line = line.strip()
        self.chunks: None | List[str] = None

    def syntax_error_score(self) -> int:
        self.chunks = []
        for c in self.line:
            if c in SyntaxError.CHUNK_CHARS.keys():  # if opener
                self.chunks.append(c)
            else:  # if closer
                if SyntaxError.CHUNK_CHARS[self.chunks.pop()] != c:
                    self.chunks = None
                    return SyntaxError.CHUNK_ERROR_POINTS[c]

        return 0

    def autocomplete_score(self) -> int | None:
        if self.chunks is None:
            return None

        score = 0
        for c in reversed(self.chunks):
            score *= 5
            score += SyntaxError.CHUNK_AUTOCOMPLETE_POINTS[
                SyntaxError.CHUNK_CHARS[c]]

        return score


def syntax(input: str) -> None:
    error_score = 0
    autocomplete_scores: List[int] = []
    with open(input) as f:
        for line in f:
            syntax = SyntaxError(line)
            error_score += syntax.syntax_error_score()
            autocomplete_score = syntax.autocomplete_score()
            if autocomplete_score:
                autocomplete_scores.append(autocomplete_score)

    autocomplete_scores.sort()

    print(f"The syntax error score is {error_score}")
    print(
        f"The autocomplete score is {autocomplete_scores[len(autocomplete_scores) // 2]}"
    )


if __name__ == "__main__":
    syntax("input")
