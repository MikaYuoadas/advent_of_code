#!/usr/bin/env python
import sys
from typing import Iterable

import numpy as np


class Board:
    def __init__(self, rows: Iterable[Iterable[int]]) -> None:
        self._board = np.array(rows)
        self._unmarked = np.ones(self._board.shape)

    def mark(self, number: int) -> None:
        for y in range(self._board.shape[1]):
            for x in range(self._board.shape[0]):
                if number == self._board[y, x]:
                    self._unmarked[y, x] = False

    def reset(self) -> None:
        self._unmarked = np.ones(self._board.shape)

    @property
    def won(self) -> bool:
        for row in self._unmarked:
            if not sum(row):
                return True

        for col in self._unmarked.T:
            if not sum(col):
                return True

        return False

    def score(self, winning_draw: int) -> int:
        score = 0
        for y in range(self._board.shape[1]):
            for x in range(self._board.shape[0]):
                if self._unmarked[y, x]:
                    score += self._board[y, x]
        return score * winning_draw


def parse(filename: str) -> tuple[list[int], list[Board]]:
    with open(filename) as f:
        draws = [int(x) for x in f.readline().strip().split(',')]
        f.readline()

        boards = []
        rows = []
        for line in f:
            row = [int(x) for x in line.strip().split() if x]
            if not row:
                boards.append(Board(rows))
                rows = []
                continue
            rows.append(row)
        boards.append(Board(rows))

    return draws, boards


def main(filename: str) -> None:
    draws, boards = parse(filename)

    score = 0
    for draw in draws:
        for board in boards:
            board.mark(draw)
            if board.won:
                score = board.score(draw)
                break
        else:
            continue
        break
    print(f'Step 1: {score}')

    for board in boards:
        board.reset()

    score = 0
    for draw in draws:
        for board in boards:
            board.mark(draw)
        remaining_boards = [board for board in boards if not board.won]
        if not remaining_boards:
            assert len(boards) == 1
            score = boards[0].score(draw)
            break
        boards = remaining_boards
    print(f'Step 2: {score}')


if __name__ == '__main__':
    main(sys.argv[1])
