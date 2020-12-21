#!/usr/bin/env python
import sys
from typing import List


def parse(filename: str) -> List[int]:
    with open(filename) as f:
        return list(map(int, f.read().split(',')))


def play(init_sequence: List[int], stop: int) -> int:
    memory = {}
    for i, n in enumerate(init_sequence[:-1]):
        memory[n] = i

    next_n = init_sequence[-1]
    for turn in range(i + 1, stop):
        n = next_n
        try:
            next_n = turn - memory[n]
        except KeyError:
            next_n = 0
        memory[n] = turn
    return n


def main(filename: str) -> None:
    numbers = parse(filename)

    n = play(numbers, 2020)
    print(f'Step 1: {n}')

    n = play(numbers, 30000000)
    print(f'Step 2: {n}')


if __name__ == '__main__':
    main(sys.argv[1])
