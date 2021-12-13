#!/usr/bin/env python
import re
from argparse import ArgumentParser
from enum import auto, Enum
from typing import NamedTuple

import numpy as np


class Dot(NamedTuple):
    x: int
    y: int


class Direction(Enum):
    up = auto()
    left = auto()


class Fold(NamedTuple):
    direction: Direction
    value: int


def parse(filename: str) -> tuple[tuple[int, int], list[Dot], list[Fold]]:
    with open(filename, 'r') as f:
        dots = []
        folds = []
        x_max, y_max = 0, 0
        for line in f:
            if line.isspace():
                break
            x, y = line.strip().split(',')
            x_max, y_max = max(int(x), x_max), max(int(y), y_max)
            dots.append(Dot(int(x), int(y)))
        for line in f:
            m = re.match(r'fold along ([xy])=(\d+)', line)
            if not m:
                raise ValueError(f'Can\'t parse input file {filename}')
            folds.append(Fold(Direction.up if m[1] == 'y' else Direction.left,
                         int(m[2])))
    return (x_max + 1, y_max + 1), dots, folds


class Paper:
    def __init__(self, size: tuple[int, int]) -> None:
        self._size = size
        self.dots: set[Dot] = set()

    def __str__(self) -> str:
        return '\n'.join(''.join('#' if (x, y) in self.dots else '.'
                                 for x in range(self._size[0]))
                         for y in range(self._size[1]))

    def mark(self, dot: Dot) -> None:
        if dot.x > self._size[0] or dot.y > self._size[1]:
            raise ValueError('Dot ({dot.x}, {dot.y}) outside paper!')
        self.dots.add(dot)

    def fold(self, fold: Fold) -> None:
        new_dots = set()
        w, h = 0, 0
        for dot in self.dots:
            if fold.direction == Direction.up and dot.y > fold.value:
                dot = Dot(dot.x, 2 * fold.value - dot.y)
            elif fold.direction == Direction.left and dot.x > fold.value:
                dot = Dot(2 * fold.value - dot.x, dot.y)
            new_dots.add(dot)
            w, h = max(w, dot.x), max(h, dot.y)
        self._size = (w + 1, h + 1)
        self.dots = new_dots


def main(filename: str, verbose: int) -> None:
    size, dots, folds = parse(filename)

    paper = Paper(size)
    for i, dot in enumerate(dots):
        if verbose > 1:
            print(paper)
            print()
            print(f'Dot {i + 1}')
        paper.mark(dot)
    if verbose:
        print(paper)
        print()

    for i, fold in enumerate(folds, start=1):
        paper.fold(fold)
        if verbose:
            print(f'Paper after fold {i}')
            print(paper)
            print()
        if i == 1:
            dots_first_fold = len(paper.dots)

    print('Final paper:')
    print(paper)
    print(f'\nStep 1: number of dots after first fold: {dots_first_fold}')
    print('Step 2: Read code final paper above')


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('filename')
    parser.add_argument('--verbose', '-v', action='count', default=0)
    args = parser.parse_args()
    try:
        main(args.filename, args.verbose)
    except KeyboardInterrupt:
        pass
