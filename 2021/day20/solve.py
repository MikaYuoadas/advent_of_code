#!/usr/bin/env python
from argparse import ArgumentParser
from math import inf
from typing import NewType

import numpy as np


Algorithm = NewType('Algorithm', list[int])


class Image:
    def __init__(self, pixels: np.ndarray) -> None:
        self.canvas = pixels
        self.background = 0

    def grow_canvas(self, border: int) -> None:
        self.canvas = np.pad(
            self.canvas,
            (border,),
            constant_values=(self.background,),
        )

    def count_lit_pixels(self) -> float:
        if self.background:
            return inf
        return sum(self.canvas.flatten())

    def enhance(self, algo: Algorithm) -> None:
        self.grow_canvas(1)  # FIXME: can't we be clever than that?
        new_canvas = np.copy(self.canvas)
        for y in range(1, self.canvas.shape[0] - 1):
            for x in range(1, self.canvas.shape[1] - 1):
                index = int(
                    ''.join(
                        str(p)
                        for p in self.canvas[y-1:y+2, x-1:x+2].flatten()
                    ),
                    2,
                )
                new_canvas[y, x] = algo[index]

        # Handle virtually infinite canvas
        self.background = algo[int(str(self.background) * 9, 2)]
        new_canvas[0, :] = self.background
        new_canvas[-1, :] = self.background
        new_canvas[:, 0] = self.background
        new_canvas[:, -1] = self.background

        self.canvas = new_canvas

    def __str__(self) -> str:
        return '\n'.join(
            ''.join(
                '#' if p else '.'
                for p in line
            )
            for line in self.canvas
        )


def parse(filename: str) -> tuple[Algorithm, Image]:
    with open(filename, 'r') as f:
        algo = Algorithm([int(c == '#') for c in f.readline().strip()])
        f.readline()
        dat = np.array([[int(c == '#') for c in line.strip()] for line in f])
        img = Image(dat)
        img.grow_canvas(2)
    return algo, img


def main(filename: str, verbose: int) -> None:
    algo, img = parse(filename)

    if verbose:
        print(f'Initial image:\n{img}')
    for i in range(50):
        img.enhance(algo)
        if verbose > 1:
            print(f'\nAfter {i + 1} enhances:\n{img}')
        if i == 1:
            step1_res = img.count_lit_pixels()
    if verbose:
        print(f'\nFinal image:\n{img}')
    print(f'\nStep 1: lit pixels after 2 enhances: {step1_res}')
    print(f'Step 2: lit pixels after 50 enhances: {img.count_lit_pixels()}')


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('filename')
    parser.add_argument('--verbose', '-v', action='count', default=0)
    args = parser.parse_args()
    try:
        main(args.filename, args.verbose)
    except KeyboardInterrupt:
        pass
