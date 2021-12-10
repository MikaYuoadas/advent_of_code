#!/usr/bin/env python
from argparse import ArgumentParser
from functools import cached_property
from math import prod
from typing import Iterator, NamedTuple


class Point(NamedTuple):
    x: int
    y: int

    def __repr__(self):
        return str((self.x, self.y))


def parse(filename: str) -> dict[Point, int]:
    with open(filename) as f:
        return {
            Point(x, y): int(v)
            for y, line in enumerate(f)
            for x, v in enumerate(line.strip())
        }

class HeightMap:
    def __init__(self, heights: dict[Point, int]):
        self.heights = heights

    @cached_property
    def low_points(self) -> list[Point]:
        low_points = []
        for p, h in self.heights.items():
            if h < min(*(self.heights[n] for n in self.neighbors(p))):
                low_points.append(p)
        return low_points

    def neighbors(self, p: Point) -> Iterator[Point]:
        return (
            n for n in [
                Point(p.x - 1, p.y),
                Point(p.x + 1, p.y),
                Point(p.x, p.y - 1),
                Point(p.x, p.y + 1),
            ]
            if n in self.heights)

    @cached_property
    def risk_level(self) -> int:
        risk_level = 0
        for point in self.low_points:
            risk_level += 1 + self.heights[point]
        return risk_level

    @cached_property
    def basins(self) -> list[set[Point]]:
        basins = []
        for low_point in self.low_points:
            basin = set()
            todo = {low_point}
            while todo:
                p = todo.pop()
                if self.heights[p] < 9:
                    basin.add(p)
                    todo.update(set(self.neighbors(p)) - basin)
            basins.append(basin)
        return sorted(basins, key=len)


def main(filename: str, verbose: int) -> None:
    heights = parse(filename)
    heightmap = HeightMap(heights)

    print(f'Step 1: {heightmap.risk_level}')
    print(f'Step 2: {prod(map(len, heightmap.basins[-3:]))}')


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('filename')
    parser.add_argument('--verbose', '-v', action='count', default=0)
    args = parser.parse_args()
    try:
        main(args.filename, args.verbose)
    except KeyboardInterrupt:
        pass
