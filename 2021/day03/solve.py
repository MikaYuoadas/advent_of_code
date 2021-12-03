#!/usr/bin/env python
import sys
from dataclasses import dataclass
from math import inf
from typing import Iterable, Optional

import numpy as np


def parse(filename: str) -> np.ndarray:
    with open(filename) as f:
        report = np.array([[int(bit) for bit in line.strip()] for line in f])

    return report


def get_power(report: np.ndarray) -> tuple[int, int]:
    bits = [sum(col) > len(col) / 2 for col in report.T]
    gamma = int(''.join('1' if b else '0' for b in bits), 2)
    epsilon = int(''.join('0' if b else '1' for b in bits), 2)
    return gamma, epsilon


def get_life_support(report: np.ndarray) -> tuple[int, int]:
    tree = Node()
    for line in report:
        tree.add(line)

    return int(tree.get_o2_bits(), 2), int(tree.get_co2_bits(), 2)


@dataclass
class Node:
    one: Optional['Node'] = None
    zero: Optional['Node'] = None
    size: int = 0

    def add(self, number: Iterable[int]) -> None:
        self.size += 1
        rest = iter(number)
        try:
            head = next(rest)
        except StopIteration:
            return
        if head:
            self.one = self.one or Node()
            self.one.add(rest)
        else:
            self.zero = self.zero or Node()
            self.zero.add(rest)

    def get_o2_bits(self) -> str:
        ones = self.one and self.one.size or 0
        zeros = self.zero and self.zero.size or 0

        if 0 < ones >= zeros:
            return '1' + self.one.get_o2_bits()
        elif 0 < zeros > ones:
            return '0' + self.zero.get_o2_bits()
        else:
            return ''

    def get_co2_bits(self) -> str:
        ones = self.one and self.one.size or inf
        zeros = self.zero and self.zero.size or inf

        if inf > zeros <= ones:
            return '0' + self.zero.get_co2_bits()
        elif inf > ones < zeros:
            return '1' + self.one.get_co2_bits()
        else:
            return ''


def main(filename: str) -> None:
    report = parse(filename)

    gamma, epsilon = get_power(report)
    print(f'Step 1: power consumption = {gamma * epsilon}')

    o2, co2 = get_life_support(report)
    print(f'Step 2: life support = {o2 * co2}')


if __name__ == '__main__':
    main(sys.argv[1])
