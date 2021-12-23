#!/usr/bin/env python
import re
from argparse import ArgumentParser
from collections import OrderedDict
from typing import NamedTuple, Optional


class Cuboid(NamedTuple):
    x: tuple[int, int]
    y: tuple[int, int]
    z: tuple[int, int]

    @property
    def size(self) -> int:
        return (
            abs(self.x[1] - self.x[0] + 1)
            * abs(self.y[1] - self.y[0] + 1)
            * abs(self.z[1] - self.z[0] + 1)
        )

    def __and__(self, other: 'Cuboid') -> Optional['Cuboid']:
        if not isinstance(other, type(self)):
            raise TypeError(
                f'unsupported operand type(s) for &: '
                f'\'{type(self)}\' and \'{type(other)}\''
            )
        c = type(self)(
            (max(self.x[0], other.x[0]), min(self.x[1], other.x[1])),
            (max(self.y[0], other.y[0]), min(self.y[1], other.y[1])),
            (max(self.z[0], other.z[0]), min(self.z[1], other.z[1])),
        )
        if c.x[0] <= c.x[1] and c.y[0] <= c.y[1] and c.z[0] <= c.z[1]:
            return c
        else:
            return None

    def __contains__(self, other: object) -> bool:
        if not isinstance(other, type(self)):
            return False
        return (
            self.x[0] <= other.x[0] and self.x[1] >= other.x[1]
            and self.y[0] <= other.y[0] and self.y[1] >= other.y[1]
            and self.z[0] <= other.z[0] and self.z[1] >= other.z[1]
        )

    def __sub__(self, other: 'Cuboid') -> list['Cuboid']:
        if not isinstance(other, type(self)):
            raise TypeError(
                f'unsupported operand type(s) for -: '
                f'\'{type(self)}\' and \'{type(other)}\''
            )

        if not self & other:
            return [self]

        old = self
        splitted: list['Cuboid'] = []
        for axis in ('x', 'y', 'z'):
            new, old = old.split(axis, getattr(other, axis)[0])
            if new:
                splitted.append(new)
            if not old:
                break

            old, new = old.split(axis, getattr(other, axis)[1] + 1)
            if new:
                splitted.append(new)
            if not old:
                break

        return splitted

    def split(
        self,
        axis: str,
        value: int
    ) -> tuple[Optional['Cuboid'], Optional['Cuboid']]:
        v_min = getattr(self, axis)[0]
        v_max = getattr(self, axis)[1]

        if value <= v_min:
            return (None, self)
        if v_max < value:
            return (self, None)

        return (
            Cuboid(
                *(
                    (v_min, value - 1)
                    if d == axis
                    else getattr(self, d)
                    for d in ('x', 'y', 'z')
                )
            ),
            Cuboid(
                *(
                    (value, v_max)
                    if d == axis
                    else getattr(self, d)
                    for d in ('x', 'y', 'z')
                )
            ),
        )


class Core:
    def __init__(self) -> None:
        self.cuboids: list[Cuboid] = []

    def turn(self, c: Cuboid, on: bool) -> None:
        new_cuboids = []
        for old in self.cuboids:
            if old & c:
                new_cuboids.extend(old - c)
            else:
                new_cuboids.append(old)
        if on:
            new_cuboids.append(c)
        self.cuboids = new_cuboids

    @property
    def cubes_on(self) -> int:
        return sum(c.size for c in self.cuboids)

    def __and__(self, other: Cuboid) -> 'Core':
        new_core = type(self)()
        for cuboid in self.cuboids:
            if c := cuboid & other:
                new_core.cuboids.append(c)
        return new_core


def parse(filename: str) -> OrderedDict[Cuboid, bool]:
    with open(filename, 'r') as f:
        return OrderedDict(
            (
                Cuboid(
                    (int(m[2]), int(m[3])),
                    (int(m[4]), int(m[5])),
                    (int(m[6]), int(m[7])),
                ),
                m[1] == 'on',
            )
            for line in f
            if (m := re.match(
                r'(on|off) '
                r'x=(-?\d+)..(-?\d+),'
                r'y=(-?\d+)..(-?\d+),'
                r'z=(-?\d+)..(-?\d+)',
                line,
            ))
        )


def main(filename: str, verbose: int) -> None:
    procedure = parse(filename)

    core = Core()
    for cuboid, state in procedure.items():
        core.turn(cuboid, state)
    print(f'Step 1: cubes ON in region: '
          f'{(core & Cuboid((-50, 50), (-50, 50), (-50, 50))).cubes_on}')
    print(f'Step 2: total cubes ON: {core.cubes_on}')


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('filename')
    parser.add_argument('--verbose', '-v', action='count', default=0)
    args = parser.parse_args()
    try:
        main(args.filename, args.verbose)
    except KeyboardInterrupt:
        pass
