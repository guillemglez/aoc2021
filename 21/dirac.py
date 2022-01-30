from typing import Dict, Final, List, NewType, Tuple


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


class Quantum:
    Position = NewType("Position", Tuple[int, int])
    Score = NewType("Score", Tuple[int, int])
    Wins = NewType("Wins", Tuple[int, int])
    Cache = NewType("Cache", Dict[Position, Dict[Score, Wins]])

    DICE: Final = (1, 2, 3)
    WINNER_SCORE: Final = 21

    def __init__(self, starting_positions: Position) -> None:
        self.pos = starting_positions
        self.score = Quantum.Score((0, 0))
        self.dice: Dict[int, int] = {}
        self.cache: Quantum.Cache = Quantum.Cache({})
        self.simdice()

    def compute(self) -> int:
        wins = self.wins(self.pos, self.score)
        return max(wins)

    def wins(self, pos: Position, scores: Score) -> Wins:
        if pos in self.cache.keys() and scores in self.cache[pos].keys():
            return self.cache[pos][scores]

        if scores[1] >= Quantum.WINNER_SCORE:
            return Quantum.Wins((1, 0))

        wins = Quantum.Wins((0, 0))
        for roll, frequency in self.dice.items():
            lands = (pos[0] + roll - 1) % Board.BOARD_SIZE + 1
            outcome = self.wins(Quantum.Position((pos[1], lands)),
                                Quantum.Score((scores[1], scores[0] + lands)))

            wins = Quantum.Wins((wins[0] + outcome[1] * frequency,
                                 wins[1] + outcome[0] * frequency))

        if pos not in self.cache.keys():
            self.cache[pos] = {}

        self.cache[pos][scores] = wins
        return wins

    def simdice(self, score=0, rolls=3) -> None:
        if rolls == 0:
            if score in self.dice.keys():
                self.dice[score] += 1
            else:
                self.dice[score] = 1
            return

        for roll in Quantum.DICE:
            self.simdice(score + roll, rolls - 1)


def dirac(input: str) -> None:
    board = Board()
    with open(input) as f:
        p1 = Player(board, int(f.readline().split()[-1]))
        p2 = Player(board, int(f.readline().split()[-1]))

    universes = Quantum(Quantum.Position((p1.pos, p2.pos)))

    while True:
        if p1.play() or p2.play():
            break

    print(f"Result is {board.rolls * (p1.score if p2.winner() else p2.score)}")
    print(f"Most wins in universes are {universes.compute()}")


if __name__ == "__main__":
    dirac("input")
