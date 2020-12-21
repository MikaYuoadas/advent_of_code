#!/usr/bin/env python
import sys


def parse(filename):
    with open(filename) as f:
        return [int(line) for line in f.readlines()]


def validate(n, ancestors):
    ancestors = set(ancestors)
    for i in ancestors:
        if n - i != n and (n - i) in ancestors:
            return True
    return False


def find_invalid(buf, size):
    for i in range(size, len(buf)):
        if not validate(buf[i], buf[i - size:i]):
            return buf[i]


def bruteforce(buf, target):
    for i in range(len(buf) - 1):
        for j in range(i + 2, len(buf) + 1):
            if sum(buf[i:j]) == target:
                return min(buf[i:j]) + max(buf[i:j])
    return -1


def main(filename, size):
    buf = parse(filename)
    bad_n = find_invalid(buf, size)
    print(f'Step 1: {bad_n}')

    weakness = bruteforce(buf, bad_n)
    print(f'Step 2: {weakness}')


if __name__ == '__main__':
    try:
        size = int(sys.argv[2])
    except IndexError:
        size = 25
    main(sys.argv[1], size)
