#!/usr/bin/env python
import json
from argparse import ArgumentParser
from copy import deepcopy
from dataclasses import dataclass
from itertools import permutations
from math import ceil, floor
from typing import Optional, Union


@dataclass
class SnailfishNumber:
    x: Union[int, 'SnailfishNumber']
    y: Union[int, 'SnailfishNumber']

    @classmethod
    def from_string(cls, s: str) -> 'SnailfishNumber':
        try:
            data = json.loads(s)
        except json.JSONDecodeError:
            raise ValueError(f'invalid literal for SnailfishNumber: {s}')
        else:
            return cls.from_data(data)

    @classmethod
    def from_data(cls, data: list[list | int]) -> 'SnailfishNumber':
        if not isinstance(data, list) or len(data) != 2:
            raise ValueError(f'invalid literal for SnailfishNumber: {data}')
        x, y = data
        if not isinstance(x, int):
            x = cls.from_data(x)
        if not isinstance(y, int):
            y = cls.from_data(y)
        return SnailfishNumber(x, y)

    def __str__(self) -> str:
        return f'[{self.x},{self.y}]'

    def __copy__(self) -> 'SnailfishNumber':
        return type(self)(self.x, self.y)

    def __deepcopy__(self, memo) -> 'SnailfishNumber':
        return type(self)(deepcopy(self.x), deepcopy(self.y))

    def __add__(self, other: Union['SnailfishNumber', int]) -> 'SnailfishNumber':
        if isinstance(other, type(self)):
            sn = type(self)(deepcopy(self), deepcopy(other))
            while True:
                if not sn._explode() and not sn._split():
                    break
            return sn
        elif isinstance(other, int):
            return type(self)(deepcopy(self.x), self.y + other)
        else:
            raise TypeError(
                "unsupported operand type(s) for +: "
                f"'{type(self)}' and '{type(other)}'"
            )

    def __radd__(self, other: int) -> 'SnailfishNumber':
        if not isinstance(other, int):
            raise TypeError(
                "unsupported operand type(s) for +: "
                f"'{type(other)}' and '{type(self)}'"
            )
        return type(self)(other + self.x, deepcopy(self.y))

    def _explode(
        self,
        depth: int = 0
    ) -> Optional[tuple[Optional[int], Optional[int]]]:
        if (isinstance(self.x, type(self))
                and (res := self.x._explode(depth + 1))):
            if res:
                if res[1] is not None:
                    self.y = res[1] + self.y
                    if res[0] is not None:
                        self.x = 0
                return (res[0], None)
        elif (isinstance(self.y, type(self))
              and (res := self.y._explode(depth + 1))):
            if res:
                if res[0] is not None:
                    self.x = self.x + res[0]
                    if res[1] is not None:
                        self.y = 0
                return (None, res[1])
        elif isinstance(self.x, int) and isinstance(self.y, int) and depth > 3:
            return (self.x, self.y)
        else:
            return None

    def _split(self) -> bool:
        if isinstance(self.x, type(self)) and self.x._split():
            return True
        elif isinstance(self.x, int) and self.x > 9:
            self.x = type(self)(floor(self.x / 2), ceil(self.x / 2))
            return True
        elif isinstance(self.y, type(self)) and self.y._split():
            return True
        elif isinstance(self.y, int) and self.y > 9:
            self.y = type(self)(floor(self.y / 2), ceil(self.y / 2))
            return True
        else:
            return False

    @property
    def magnitude(self) -> int:
        lmag = self.x if isinstance(self.x, int) else self.x.magnitude
        rmag = self.y if isinstance(self.y, int) else self.y.magnitude
        return 3 * lmag + 2 * rmag


def parse(filename: str) -> list[SnailfishNumber]:
    with open(filename, 'r') as f:
        return [SnailfishNumber.from_string(line.strip()) for line in f]


def main(filename: str, verbose: int) -> None:
    snailfish_numbers = parse(filename)

    total = snailfish_numbers[0]
    for sn in snailfish_numbers[1:]:
        if verbose:
            print(f'   {total}')
            print(f'+  {sn}')
        total += sn
        if verbose:
            print(f'=  {total}\n')
    print(f'Step 1: final sum magnitude: {total.magnitude}')

    max_magnitude = 0
    for a, b in permutations(snailfish_numbers, 2):
        max_magnitude = max(max_magnitude, (a + b).magnitude)
    print(f'Step 2: largest magnitude of any sum of two: {max_magnitude}')


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('filename')
    parser.add_argument('--verbose', '-v', action='count', default=0)
    args = parser.parse_args()
    try:
        main(args.filename, args.verbose)
    except KeyboardInterrupt:
        pass
