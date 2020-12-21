#!/usr/bin/env python
import sys


def parse(filename):
    with open(filename) as f:
        lines = [line.strip() for line in f.readlines()]

    return lines


def get_id(bpass):
    return int(bpass.translate(''.maketrans('BRFL', '1100')), 2)


def main(filename):
    bpasses = parse(filename)
    max_ = 0
    ids = set()
    for bp in bpasses:
        id_ = get_id(bp)
        max_ = max(max_, id_)
        ids.add(id_)

    print(f'part 1: {max_}')

    sorted_ids = sorted(ids)
    min_, max_ = sorted_ids[0], sorted_ids[-1]
    free_seat = set(range(min_ + 1, max_)) - ids
    assert len(free_seat) == 1

    print(f'part 2: {next(iter(free_seat))}')


if __name__ == '__main__':
    main(sys.argv[1])
