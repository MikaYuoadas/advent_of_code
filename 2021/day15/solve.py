#!/usr/bin/env python
from argparse import ArgumentParser
from heapq import heappop, heappush
from typing import NamedTuple

import numpy as np


class Point(NamedTuple):
    x: int
    y: int


class PriorityQueue:
    def __init__(self) -> None:
        self.elements: list[tuple[float, Point]] = []

    def push(self, item: Point, priority: float) -> None:
        heappush(self.elements, (priority, item))

    def pop(self) -> Point:
        return heappop(self.elements)[1]

    def __len__(self) -> int:
        return len(self.elements)


def manhattan(a: Point, b: Point) -> int:
    return abs(a.x - b.x) + abs(a.y - b.y)


def neighbors(p: Point, rmap: np.ndarray):
    return [
        n for n in [
            Point(p.x - 1, p.y),
            Point(p.x + 1, p.y),
            Point(p.x, p.y - 1),
            Point(p.x, p.y + 1),
        ]
        if 0 <= n.x < rmap.shape[0] and 0 <= n.y < rmap.shape[1]
    ]


def astar(rmap: np.ndarray, start: Point, end: Point) -> int:
    costs = np.ones(rmap.shape) * np.inf
    frontier = PriorityQueue()
    frontier.push(start, 0)
    costs[start] = 0

    while frontier:
        p = frontier.pop()

        if p == end:
            break

        for n in neighbors(p, rmap):
            cost = costs[p] + rmap[n]
            if cost < costs[n]:
                costs[n] = cost
                frontier.push(n, cost + manhattan(n, end))

    return int(costs[end])


def upscale(rmap: np.ndarray, factor: int) -> np.ndarray:
    w, h = rmap.shape
    out = np.zeros((w * factor, h * factor))
    for x in range(factor):
        for y in range(factor):
            out[x*w:(x+1)*w, y*h:(y+1)*h] = (rmap + x + y - 1) % 9 + 1
    return out
    return out


def parse(filename: str) -> np.ndarray:
    with open(filename, 'r') as f:
        risks = np.array([[int(risk) for risk in line.strip()] for line in f])

    return risks.T


def main(filename: str, verbose: int) -> None:
    risk_map = parse(filename)

    path_risk = astar(
        risk_map,
        start=Point(0, 0),
        end=Point(risk_map.shape[0] - 1, risk_map.shape[1] - 1),
    )
    print(f'\nStep 1: lowest total risk: {path_risk}')

    risk_map = upscale(risk_map, 5)
    path_risk = astar(
        risk_map,
        start=Point(0, 0),
        end=Point(risk_map.shape[0] - 1, risk_map.shape[1] - 1),
    )
    print(f'\nStep 2: lowest total risk: {path_risk}')


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('filename')
    parser.add_argument('--verbose', '-v', action='count', default=0)
    args = parser.parse_args()
    try:
        main(args.filename, args.verbose)
    except KeyboardInterrupt:
        pass
