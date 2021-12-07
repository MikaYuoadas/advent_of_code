#!/usr/bin/env python
from argparse import ArgumentParser
from math import inf
from statistics import median
from typing import Callable


def parse(filename: str) -> list[int]:
    with open(filename) as f:
        return [int(x) for x in f.read().strip().split(',')]


def cost1(x: int, target: int) -> int:
    return abs(x - target)


def cost2(x: int, target: int) -> int:
    d = abs(x - target)
    return d * (d + 1) // 2


def total_fuel(xs: list[int], target: int, cost: Callable) -> int:
    return sum(cost(x, target) for x in xs)


def main(filename: str, verbose: int) -> None:
    xs = parse(filename)

    median_x = int(median(xs))
    fuel = total_fuel(xs, median_x, cost1)
    print(f'Step 1: fuel to spend: {fuel}')

    fuel = inf
    for x in range(min(xs), max(xs)):
        fuel = min(fuel, total_fuel(xs, x, cost2))
    print(f'Step 2: fuel to spend: {fuel}')


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('filename')
    parser.add_argument('--verbose', '-v', action='count', default=0)
    args = parser.parse_args()
    try:
        main(args.filename, args.verbose)
    except KeyboardInterrupt:
        pass
