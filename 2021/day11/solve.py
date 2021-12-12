#!/usr/bin/env python
from argparse import ArgumentParser
from typing import NamedTuple

import numpy as np


class Point(NamedTuple):
    x: int
    y: int


def parse(filename: str) -> list[list[int]]:
    with open(filename, 'r') as f:
        return [[int(o) for o in line.strip()] for line in f]


class OctopusGrid:
    def __init__(self, octopuses: list[list[int]]) -> None:
        self._octopuses = np.array(octopuses).T

    def __str__(self) -> str:
        return '\n'.join(''.join(str(o) for o in r) for r in self._octopuses.T)

    @property
    def size(self) -> int:
        return self._octopuses.size

    def step(self) -> int:
        blinks = 0
        self._octopuses += 1
        triggered = set()
        todo = {
            Point(x, y)
            for x in range(self._octopuses.shape[0])
            for y in range(self._octopuses.shape[1])
        }
        while todo:
            p = todo.pop()
            if self._octopuses[p] > 9:
                blinks += 1
                triggered.add(p)
                self._octopuses[p] = 0
                for n in self.neighbors(p) - triggered:
                    self._octopuses[n] += 1
                    todo.add(n)

        return blinks

    def neighbors(self, p: Point) -> set[Point]:
        return {
            n
            for n in [
                Point(p.x - 1, p.y - 1),
                Point(p.x, p.y - 1),
                Point(p.x + 1, p.y - 1),
                Point(p.x - 1, p.y),
                Point(p.x + 1, p.y),
                Point(p.x - 1, p.y + 1),
                Point(p.x, p.y + 1),
                Point(p.x + 1, p.y + 1),
            ]
            if (0 <= n.x < self._octopuses.shape[0]
                and 0 <= n.y < self._octopuses.shape[1])
        }


def main(filename: str, steps: int, verbose: int) -> None:
    octopuses = parse(filename)
    grid = OctopusGrid(octopuses)
    blinks = 0
    if verbose:
        print('Before any steps:')
        print(grid)
        print()
    for i in range(1, steps + 1):
        blinks += grid.step()
        if verbose:
            print(f'After step {i}')
            print(grid)
            print()

    print(f'\nStep 1: total flashes: {blinks}')

    while True:
        i += 1
        if grid.step() == grid.size:
            break
    print(f'Step 2: first synced flash at step {i}')


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('filename')
    parser.add_argument('--verbose', '-v', action='count', default=0)
    parser.add_argument('--steps', '-s', default=100)
    args = parser.parse_args()
    try:
        main(args.filename, args.steps, args.verbose)
    except KeyboardInterrupt:
        pass
