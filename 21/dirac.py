from typing import Final


class Board:
    ROLLS_PER_PLAY: Final = 3
    BOARD_SIZE: Final = 10

    def __init__(self) -> None:
        self.die = 100
        self.rolls = 0

    def roll(self) -> int:
        self.rolls += 1
        if 100 != self.die:
            self.die += 1
        else:
            self.die = 1
        return self.die

    def play(self, pos: int) -> int:
        rolls: Final = sum([self.roll() for _ in range(Board.ROLLS_PER_PLAY)])
        return (rolls + pos - 1) % Board.BOARD_SIZE + 1


class Player:
    WINNER_SCORE: Final = 1000

    def __init__(self, board: Board, starting_position: int) -> None:
        self.board = board
        self.pos = starting_position
        self.score = 0

    def play(self) -> bool:
        self.pos = self.board.play(self.pos)
        self.score += self.pos
        return self.winner()

    def winner(self) -> bool:
        return self.score >= Player.WINNER_SCORE


def dirac(input: str) -> None:
    board = Board()
    with open(input) as f:
        p1 = Player(board, int(f.readline().split()[-1]))
        p2 = Player(board, int(f.readline().split()[-1]))

    while True:
        if p1.play() or p2.play():
            break

    print(f"Result is {board.rolls * (p1.score if p2.winner() else p2.score)}")


if __name__ == "__main__":
    dirac("input")
