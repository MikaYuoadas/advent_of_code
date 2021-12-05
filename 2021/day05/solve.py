#!/usr/bin/env python
import re
from argparse import ArgumentParser
from collections import Counter, namedtuple
from os.path import splitext
from typing import Iterable, Optional, TypeVar

import numpy as np
from PIL import Image


Point = namedtuple('Point', ('x', 'y'))
Line = namedtuple('Line', ('start', 'end'))
T = TypeVar('T')

def lerp(a: T, b: T, t: float) -> T:
    return a * (1 - t) + b * t


class Map:
    _color_min = np.array([0, 255, 0])
    _color_max = np.array([255, 0, 0])

    def __init__(self,
                 vent_lines: Optional[Iterable[Line]] = None,
                 ignore_diags: bool = False) -> None:
        self.width = 0
        self.height = 0
        self.vents = Counter()
        if vent_lines:
            for vent_line in vent_lines:
                self.add_vents(vent_line, ignore_diags=ignore_diags)

    def add_vents(self, line: Line, ignore_diags: bool = False) -> None:
        if line.start.x == line.end.x:
            for y in range(min(line.start.y, line.end.y),
                           max(line.start.y, line.end.y) + 1):
                self.vents[Point(line.start.x, y)] += 1
        elif line.start.y == line.end.y:
            for x in range(min(line.start.x, line.end.x),
                           max(line.start.x, line.end.x) + 1):
                self.vents[Point(x, line.start.y)] += 1
        elif not ignore_diags:
            x_step = line.end.x > line.start.x or -1
            y_step = line.end.y > line.start.y or -1
            for x, y in zip(range(line.start.x,
                                  line.end.x + x_step,
                                  x_step),
                            range(line.start.y,
                                  line.end.y + y_step,
                                  y_step)):
                self.vents[Point(x, y)] += 1

        self.width = max(self.width, max(line.start.x, line.end.x) + 1)
        self.height = max(self.height, max(line.start.y, line.end.y) + 1)

    def overlaps(self, n: int = 2) -> list[Point]:
        points = []
        for point, count in self.vents.most_common():
            if count < n:
                break
            points.append(point)
        return points

    def save_png(self, filename: str) -> None:
        data = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        max_count = self.vents.most_common(1)[0][1]
        for point, count in self.vents.items():
            data[point.x, point.y] = lerp(self._color_min,
                                          self._color_max,
                                          (count - 1) / (max_count - 1))
        img = Image.fromarray(data, 'RGB')
        img.save(filename)

    def __str__(self) -> str:
        lines = []
        for y in range(self.height):
            lines.append(''.join(str(self.vents[Point(x, y)] or '.')
                                 for x in range(self.width)))
        return '\n'.join(lines)


def parse(filename: str) -> list[Line]:
    regex = re.compile(r'(\d+),(\d+) -> (\d+),(\d+)')
    with open(filename) as f:
        vent_lines = [Line(Point(int(m[1]), int(m[2])),
                           Point(int(m[3]), int(m[4])))
                      for line in f if (m := regex.match(line))]
    return vent_lines


def main(filename: str, verbose: int, output: Optional[str] = None) -> None:
    vent_lines = parse(filename)

    map = Map()
    for vent_line in vent_lines:
        map.add_vents(vent_line, ignore_diags=True)
        if verbose > 1:
            input(f'{map}\n')
    if verbose == 1:
        print(f'\n{map}\n')
    print(f'Step 1: {len(map.overlaps(2))}')
    if output:
        map.save_png(f'{output}_nodiags.png')

    map = Map()
    for vent_line in vent_lines:
        map.add_vents(vent_line)
        if verbose > 1:
            input(f'{map}\n')
    if verbose == 1:
        print(f'\n{map}\n')
    print(f'Step 2: {len(map.overlaps(2))}')
    if output:
        map.save_png(f'{output}.png')


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('filename')
    parser.add_argument('--verbose', '-v', action='count', default=0)
    parser.add_argument('--output', '-o')
    args = parser.parse_args()
    if args.output:
        outfile, ext = splitext(args.output)
        if ext and ext != '.png':
            parser.error('output file must be png')
    else:
        outfile = None
    try:
        main(args.filename, args.verbose, outfile)
    except KeyboardInterrupt:
        pass
