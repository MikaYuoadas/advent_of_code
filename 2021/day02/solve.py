#!/usr/bin/env python
import sys
from collections import namedtuple

import numpy as np


Command = namedtuple('Command', ('direction', 'amount'))


def parse(filename: str) -> list[Command]:
    with open(filename) as f:
        cmds = [Command(line.split()[0], int(line.split()[1])) for line in f]

    return cmds


def apply1(cmds: list[Command], pos: np.ndarray) -> np.ndarray:
    for cmd in cmds:
        if cmd.direction == 'forward':
            pos += np.array([cmd.amount, 0])
        elif cmd.direction == 'down':
            pos += np.array([0, cmd.amount])
        elif cmd.direction == 'up':
            pos += np.array([0, -cmd.amount])
        else:
            raise ValueError(f'Unknown command {cmd.direction}')
    return pos


def apply2(cmds: list[Command], pos: np.ndarray) -> np.ndarray:
    for cmd in cmds:
        if cmd.direction == 'forward':
            pos += np.array([cmd.amount, pos[2] * cmd.amount, 0])
        elif cmd.direction == 'down':
            pos += np.array([0, 0, cmd.amount])
        elif cmd.direction == 'up':
            pos += np.array([0, 0, -cmd.amount])
        else:
            raise ValueError(f'Unknown command {cmd.direction}')
    return pos
    pass


def main(filename: str) -> None:
    cmds = parse(filename)

    pos = np.zeros(2)
    pos = apply1(cmds, pos)

    print(f'Step 1: x * y = {int(pos[0] * pos[1])}')

    pos = np.zeros(3)
    pos = apply2(cmds, pos)

    print(f'Step 2: x * y = {int(pos[0] * pos[1])}')


if __name__ == '__main__':
    main(sys.argv[1])
