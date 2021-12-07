#!/usr/bin/env python
from argparse import ArgumentParser
from typing import Iterator

from collections import Counter


def parse(filename: str) -> Counter:
    with open(filename) as f:
        return Counter(int(n) for n in f.read().strip().split(','))


class School:
    def __init__(self, fishes: Counter) -> None:
        self._fishes = fishes

    def step_day(self) -> None:
        new_fishes = Counter()
        for age, count in self._fishes.items():
            if age:
                new_fishes[age - 1] += count
            else:
                new_fishes[6] += count
                new_fishes[8] += count
        self._fishes = new_fishes

    @property
    def size(self) -> int:
        return sum(self._fishes.values())

    @property
    def fishes(self) -> Iterator[int]:
        return self._fishes.elements()


def main(filename: str, days: int, verbose: int) -> None:
    fishes = parse(filename)

    school = School(fishes)
    if verbose:
        print(f'Initial state: '
              f'{",".join(str(fish) for fish in school.fishes)}')
    for day in range(days):
        school.step_day()
        if verbose:
            print(f'After {day + 1:2d} days: '
                  f'{",".join(str(fish) for fish in school.fishes)}')
    print(f'laternfish after {days} days: {school.size}')


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('filename')
    parser.add_argument('--verbose', '-v', action='count', default=0)
    parser.add_argument('--days', '-d', default=80, type=int)
    args = parser.parse_args()
    try:
        main(args.filename, args.days, args.verbose)
    except KeyboardInterrupt:
        pass
