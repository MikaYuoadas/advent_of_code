#!/usr/bin/env python
import re
from argparse import ArgumentParser
from itertools import product
from math import floor, sqrt
from typing import NamedTuple


class Velocity(NamedTuple):
    x: int
    y: int

    def __add__(self, v: 'Velocity') -> 'Velocity':
        if not isinstance(v, Velocity):
            raise TypeError(
                f'unsupported operand type(s) for +: Point and {type(v)}',
            )
        return Velocity(self.x + v.x, self.y + v.y)


class Point(NamedTuple):
    x: int
    y: int

    def __add__(self, v: Velocity) -> 'Point':
        if not isinstance(v, Velocity):
            raise TypeError(
                f'unsupported operand type(s) for +: Point and {type(v)}',
            )
        return Point(self.x + v.x, self.y + v.y)


class Target(NamedTuple):
    x_min: int
    x_max: int
    y_min: int
    y_max: int

    def __contains__(self, p: Point) -> bool:
        if not isinstance(p, Point):
            raise TypeError(
                f'unsupported type: {type(p)}',
            )
        return (self.x_min <= p.x <= self.x_max
                and self.y_min <= p.y <= self.y_max)


def parse(filename: str) -> Target:
    with open(filename, 'r') as f:
        m = re.match(
            r'target area: x=(-?\d+)\.\.(-?\d+), y=(-?\d+)\.\.(-?\d+)',
            f.read().strip(),
        )
        if not m:
            raise ValueError('Bad file format!')
        return Target(int(m[1]), int(m[2]), int(m[3]), int(m[4]))


def throw_highest_point(target: Target) -> int:
    assert target.y_min < 0
    vy = -target.y_min - 1
    y = 0
    while vy:
        y += vy
        vy -= 1
    return y


def calculate_shots(t: Target) -> list[Velocity]:
    vxs = range(floor((sqrt(8 * t.x_min + 1) - 1) / 2), t.x_max + 1)
    vys = range(t.y_min, 1 - t.y_min)

    return [v
            for vx, vy in product(vxs, vys)
            if hit(v := Velocity(vx, vy), t)]

def hit(v: Velocity, t: Target) -> bool:
    p = Point(0, 0)
    while True:
        if p in t:
            return True
        elif p.y < t.y_min:
            # We overshot target
            return False
        p += v
        v += Velocity(0, -1)
        if v.x > 0:
            v += Velocity(-1, 0)


def main(filename: str, verbose: int) -> None:
    target = parse(filename)

    peak = throw_highest_point(target)
    print(f'\nStep 1: peak: {peak}\n')

    shots = calculate_shots(target)
    if verbose:
        print(' '.join(f'{s.x},{s.y}' for s in shots))
    print(f'Step 2: possible shots: {len(shots)}')


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('filename')
    parser.add_argument('--verbose', '-v', action='count', default=0)
    args = parser.parse_args()
    try:
        main(args.filename, args.verbose)
    except KeyboardInterrupt:
        pass
