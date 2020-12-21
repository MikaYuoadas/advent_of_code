#!/usr/bin/env python
import re
import sys
from itertools import product
from collections import defaultdict, namedtuple
from typing import List, Tuple


Instruction = namedtuple('Instruction', ('cmd', 'arg', 'value'))


def parse(filename: str) -> List[Instruction]:
    with open(filename) as f:
        prog = [Instruction(m['cmd'], m['arg'], m['value'])
                for line in f.readlines()
                for m in [re.match(r'(?P<cmd>\w+)(\[(?P<arg>\d+)\])? = (?P<value>\w+)', line)]]
    return prog


def generate_masks(value: str) -> Tuple[int, int]:
    return int(value.replace('X', '1'), 2), int(value.replace('X', '0'), 2)


def init(mem: dict, prog: List[Instruction]) -> None:
    mask0, mask1 = 2**36 - 1, 0
    for inst in prog:
        if inst.cmd == 'mask':
            mask0, mask1 = generate_masks(inst.value)
            m = inst.value
        elif inst.cmd == 'mem':
            mem[inst.arg] = int(inst.value) & mask0 | mask1
        else:
            raise RuntimeError(f'Illegal instruction "{inst.cmd}!"')

def init2(mem: dict, prog: List[Instruction]) -> None:
    mask, mask1 = '0' * 36, 0
    for inst in prog:
        if inst.cmd == 'mask':
            mask = inst.value
            _, mask1 = generate_masks(inst.value)
        elif inst.cmd == 'mem':
            base_addr = int(inst.arg) | mask1
            addrs = map(''.join,
                        product(*('01' if m == 'X' else a
                                  for m, a in zip(mask, f'{base_addr:036b}'))))
            for addr in addrs:
                mem[addr] = int(inst.value)
        else:
            raise RuntimeError(f'Illegal instruction "{inst.cmd}!"')


def main(filename: str) -> None:
    prog = parse(filename)

    mem = defaultdict(int)
    init(mem, prog)
    total = sum(mem.values())
    print(f'Step 1: {total}')

    mem = defaultdict(int)
    init2(mem, prog)
    total = sum(mem.values())
    print(f'Step 2: {total}')


if __name__ == '__main__':
    main(sys.argv[1])
