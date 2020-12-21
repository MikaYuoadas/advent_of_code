#!/usr/bin/env python
import sys
from functools import partial
from operator import itemgetter
from typing import List, Tuple


def parse(filename: str) -> Tuple[int, List[str]]:
    with open(filename) as f:
        inp = f.read().split()

    return int(inp[0]), [bus for bus in inp[1].split(',')]


def next_eta(now: int, bus: int) -> int:
    return (bus - (now % bus)) % bus


def sync_time(cond: List[Tuple[int, int]]) -> int:
    t = 0
    increment = 1
    for i, bus in cond:
        while (t + i) % bus:
            t += increment
        increment *= bus
    return t


def main(filename: str) -> None:
    now, buses = parse(filename)
    bus_ids = list(map(int, filter(lambda b: b != 'x', buses)))
    next_bus, wait = min(zip(bus_ids,
                             map(partial(next_eta, now), bus_ids)),
                         key=itemgetter(1))
    print(f'Step 1: {next_bus * wait}')

    t = sync_time([(i, int(bus))
                   for i, bus in enumerate(buses)
                   if bus != 'x'])
    print(f'Step 2: {t}')


if __name__ == '__main__':
    main(sys.argv[1])
