#!/usr/bin/env python
import sys
from collections import defaultdict
from itertools import product
from typing import Set, Tuple


def parse(filename: str, d: int) -> Set[Tuple[int, ...]]:
    cubes = set()
    with open(filename) as f:
        for y, line in enumerate(f.readlines()):
            for x, state in enumerate(line):
                if state != '#':
                    continue
                cubes.add((x, y) + (0,) * (d - 2))
    return cubes


def step(cubes: Set[Tuple[int, ...]], d: int) -> Set[Tuple[int, ...]]:
    neighbors = defaultdict(int)
    for coords in cubes:
        for offsets in product(*((-1, 0, 1),) * d):
            if any(o != 0 for o in offsets):
                neighbors[tuple(c + o for c, o in zip(coords, offsets))] += 1

    new_cubes = set()
    for coords, count in neighbors.items():
        if count == 3 or (count == 2 and coords in cubes):
            new_cubes.add(coords)

    return new_cubes


def main(filename: str) -> None:
    cubes = parse(filename, 3)
    for _ in range(6):
        cubes = step(cubes, 3)
    print(f'Step 1: {len(cubes)}')

    cubes = parse(filename, 4)
    for _ in range(6):
        cubes = step(cubes, 4)
    print(f'Step 2: {len(cubes)}')


if __name__ == '__main__':
    main(sys.argv[1])
