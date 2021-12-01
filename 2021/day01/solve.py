#!/usr/bin/env python
import sys


def parse(filename: str) -> list[int]:
    depths = []
    with open(filename) as f:
        for line in f.readlines():
            depths.append(int(line))

    return depths


def main(filename: str) -> None:
    depths = parse(filename)

    n_increase = sum(n > p for n, p in zip(depths[1:], depths[:-1]))
    print(f'Number of measurements larger than the previous one: {n_increase}')

    n_increase = sum(b + c + d > a + b + c
                     for a, b, c, d in zip(depths[:-3],
                                           depths[1:-2],
                                           depths[2:-1],
                                           depths[3:]))
    print(f'Number of sliding windows larger than '
          f'the previous one: {n_increase}')


if __name__ == '__main__':
    main(sys.argv[1])
