#!/usr/bin/env python
import sys
from copy import deepcopy
from operator import methodcaller
from typing import List


EMPTY, OCCUPIED = 'L', '#'
ADJACENT, SIGHT = range(2)


class CellularAutomata:
    deltas = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))

    def __init__(self, grid: List[List[str]], strat: int, threshold: int) -> None:
        self.grid = grid
        self.neighbors = [[0] * len(grid[0]) for _ in range(len(grid))]
        self.threshold = threshold
        self.heigh = len(self.grid)
        self.width = len(self.grid[0])
        if strat == ADJACENT:
            self.recount_neighbors = self.count_adjacent_neighbors
        elif strat == SIGHT:
            self.recount_neighbors = self.count_visible_neighbors
        else:
            raise ValueError('Unknown strategy')

    @classmethod
    def from_file(cls, filename: str, strat: int, threshold: int) -> 'CellularAutomata':
        with open(filename) as f:
            return cls([list(line.strip()) for line in f.readlines()], strat, threshold)

    def step(self) -> int:
        changes = 0
        for y in range(self.heigh):
            for x in range(self.width):
                if self.grid[y][x] == EMPTY and self.neighbors[y][x] == 0:
                    self.grid[y][x] = OCCUPIED
                    changes += 1
                elif self.grid[y][x] == OCCUPIED and self.neighbors[y][x] >= self.threshold:
                    self.grid[y][x] = EMPTY
                    changes += 1
        self.recount_neighbors()
        return changes

    def count_adjacent_neighbors(self) -> None:
        for y in range(self.heigh):
            for x in range(self.width):
                self.neighbors[y][x] = 0
                for r, c in self.deltas:
                    y2, x2 = y + r, x + c
                    if (0 <= y2 < self.heigh and 0 <= x2 < self.width
                            and self.grid[y2][x2] == OCCUPIED):
                        self.neighbors[y][x] += 1

    def count_visible_neighbors(self) -> None:
        for y in range(self.heigh):
            for x in range(self.width):
                self.neighbors[y][x] = 0
                for r, c in self.deltas:
                    y2, x2 = y + r, x + c
                    while 0 <= y2 < self.heigh and 0 <= x2 < self.width:
                        if self.grid[y2][x2] == OCCUPIED:
                            self.neighbors[y][x] += 1
                            break
                        elif self.grid[y2][x2] == EMPTY:
                            break
                        y2 += r
                        x2 += c

    def count(self, state):
        return sum(map(methodcaller('count', state), self.grid))

    def __str__(self) -> str:
        return '\n'.join(''.join(row) for row in self.grid)


def main(filename: str) -> None:
    ca = CellularAutomata.from_file(filename, ADJACENT, 4)
    changes = 1
    while changes:
        changes = ca.step()

    occupied = ca.count(OCCUPIED)
    print(f'Step 1: {occupied}')

    ca = CellularAutomata.from_file(filename, SIGHT, 5)
    changes = 1
    while changes:
        changes = ca.step()

    occupied = ca.count(OCCUPIED)
    print(f'Step 2: {occupied}')


if __name__ == '__main__':
    main(sys.argv[1])
