#!/usr/bin/env python
import sys


def parse(filename):
    with open(filename) as f:
        lines = [line.strip() for line in f.readlines()]

    groups = []
    group = []
    for line in lines:
        if not line:
            groups.append(group)
            group = []
        else:
            group.append(line)

    return groups


def count_any_yes(groups):
    count = 0
    for group in groups:
        answers = set()
        for line in group:
            answers |= set(line)
        count += len(answers)

    return count


def count_unanimous_yes(groups):
    count = 0
    for group in groups:
        answers = set('abcdefghijklmnopqrstuvwxyz')
        for line in group:
            answers &= set(line)
        count += len(answers)

    return count


def main(filename):
    groups = parse(filename)
    total = count_any_yes(groups)

    print(f'part 1: {total}')

    total = count_unanimous_yes(groups)

    print(f'part 2: {total}')


if __name__ == '__main__':
    main(sys.argv[1])
