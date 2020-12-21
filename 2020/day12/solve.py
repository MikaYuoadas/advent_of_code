#!/usr/bin/env python
import sys
from typing import List, Tuple

import numpy as np


cos = lambda a: int(np.cos(np.deg2rad(a)))
sin = lambda a: int(np.sin(np.deg2rad(a)))

CMD1 = {
    'N': lambda n: np.array([[1, 0, 0, 0, 0],
                             [0, 1, 0, 0, n],
                             [0, 0, 1, 0, 0],
                             [0, 0, 0, 1, 0],
                             [0, 0, 0, 0, 1]]),
    'S': lambda n: np.array([[1, 0, 0, 0, 0],
                             [0, 1, 0, 0, -n],
                             [0, 0, 1, 0, 0],
                             [0, 0, 0, 1, 0],
                             [0, 0, 0, 0, 1]]),
    'E': lambda n: np.array([[1, 0, 0, 0, n],
                             [0, 1, 0, 0, 0],
                             [0, 0, 1, 0, 0],
                             [0, 0, 0, 1, 0],
                             [0, 0, 0, 0, 1]]),
    'W': lambda n: np.array([[1, 0, 0, 0, -n],
                             [0, 1, 0, 0, 0],
                             [0, 0, 1, 0, 0],
                             [0, 0, 0, 1, 0],
                             [0, 0, 0, 0, 1]]),
    'L': lambda n: np.array([[1, 0, 0, 0, 0],
                             [0, 1, 0, 0, 0],
                             [0, 0, cos(n), -sin(n), 0],
                             [0, 0, sin(n), cos(n), 0],
                             [0, 0, 0, 0, 1]]),
    'R': lambda n: np.array([[1, 0, 0, 0, 0],
                             [0, 1, 0, 0, 0],
                             [0, 0, cos(n), sin(n), 0],
                             [0, 0, -sin(n), cos(n), 0],
                             [0, 0, 0, 0, 1]]),
    'F': lambda n: np.array([[1, 0, n, 0, 0],
                             [0, 1, 0, n, 0],
                             [0, 0, 1, 0, 0],
                             [0, 0, 0, 1, 0],
                             [0, 0, 0, 0, 1]]),
}

# Only the translation matrices (N, S, E, W) are changed to alter the waypoint
CMD2 = dict(CMD1)
CMD2.update({
    'N': lambda n: np.array([[1, 0, 0, 0, 0],
                             [0, 1, 0, 0, 0],
                             [0, 0, 1, 0, 0],
                             [0, 0, 0, 1, n],
                             [0, 0, 0, 0, 1]]),
    'S': lambda n: np.array([[1, 0, 0, 0, 0],
                             [0, 1, 0, 0, 0],
                             [0, 0, 1, 0, 0],
                             [0, 0, 0, 1, -n],
                             [0, 0, 0, 0, 1]]),
    'E': lambda n: np.array([[1, 0, 0, 0, 0],
                             [0, 1, 0, 0, 0],
                             [0, 0, 1, 0, n],
                             [0, 0, 0, 1, 0],
                             [0, 0, 0, 0, 1]]),
    'W': lambda n: np.array([[1, 0, 0, 0, 0],
                             [0, 1, 0, 0, 0],
                             [0, 0, 1, 0, -n],
                             [0, 0, 0, 1, 0],
                             [0, 0, 0, 0, 1]]),
})


def manhattan(coord: np.ndarray) -> int:
    return (np.abs(coord[0]) + np.abs(coord[1]))[0]


def parse(filename: str) -> List[Tuple[str, int]]:
    with open(filename) as f:
        return [(line[0], int(line[1:])) for line in f.readlines()]


def main(filename: str) -> None:
    nav_plan = parse(filename)
    # x, y, east/west, north/south, 1
    coord = np.array([0, 0, 1, 0, 1]).reshape(5, 1)
    for cmd, n in nav_plan:
        coord = CMD1[cmd](n).dot(coord)
    dist = manhattan(coord)
    print(f'Step 1: {dist}')

    # x, y, east/west, north/south, 1
    coord = np.array([0, 0, 10, 1, 1]).reshape(5, 1)
    for cmd, n in nav_plan:
        coord = CMD2[cmd](n).dot(coord)
    dist = manhattan(coord)
    print(f'Step 2: {dist}')


if __name__ == '__main__':
    main(sys.argv[1])
