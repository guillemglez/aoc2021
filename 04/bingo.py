from typing import List
import numpy as np
import os

class Board:
    def __init__(self, raw_board: str) -> None:
        self.board = Board.parse_board(raw_board)
        self.marked = np.zeros(self.board.shape, dtype=bool)
        self.last: None | int = None

    @staticmethod
    def parse_board(raw_board: str) -> np.ndarray:
        board = []
        for line in raw_board.strip().split(os.linesep):
            boardline: List[int] = []
            for n in line.split():
                if len(n):
                    boardline.append(int(n))
            board.append(boardline)
        return np.array(board)

    def mark(self, n) -> bool:
        self.last = n
        self.marked[self.board == n] = True
        return self.winner()

    def winner(self) -> bool:
        rows, cols = self.marked.shape
        for r in range(rows):
            if self.marked[r, :].all():
                return True
        for c in range(cols):
            if self.marked[:, c].all():
                return True
        return False

    def score(self) -> int:
        return np.sum(self.board[np.invert(self.marked)]) * self.last


def bingo(input: str) -> None:
    boards: List[Board] = []
    with open(input) as f:
        draw = [int(n) for n in f.readline().strip().split(',')]
        if f.readline() != os.linesep:
            raise Exception("Expected empty line after draw list")

        raw_board = ""
        for line in f:
            if line != os.linesep:
                raw_board += line
            else:
                boards.append(Board(raw_board))
                raw_board = ""
        boards.append(Board(raw_board))

    winner = False
    for n in draw:
        for i, board in reversed(list(enumerate(boards))):
            if board.mark(n):
                if not winner:
                    print(f"The winner board final score is {board.score()}")
                    winner = True
                boards.pop(i)
                if len(boards) == 0:
                    print(f"The loser board final score is {board.score()}")
                    return


if __name__ == "__main__":
    bingo("input")
