#!/usr/bin/env python
import sys


def parse(filename):
    rules = {}
    with open(filename) as f:
        for line in f.readlines():
            outer, inners = line.strip().removesuffix('.').split(' contain ')
            outer = outer.rsplit(' ', 1)[0]
            if inners == 'no other bags':
                rules[outer] = {}
                continue
            inners = [i.split(' ', 1) for i in inners.split(', ')]
            rules[outer] = {i.rsplit(' ', 1)[0]: int(n) for n, i in inners}

    return rules


def can_contain(bag, color, rules):
    if (color in rules[bag]
        or any(can_contain(inner_bag, color, rules)
               for inner_bag in rules[bag])):
        return True
    else:
        return False


def count_content(bag, rules):
    if not rules[bag]:
        return 0

    count = 0
    for b, n in rules[bag].items():
        count += n * (1 + count_content(b, rules))
    return count


def main(filename):
    rules = parse(filename)
    count = 0
    for bag in rules:
        if can_contain(bag, 'shiny gold', rules):
            count += 1
    print(f'part 1: {count}')

    total = count_content('shiny gold', rules)
    print(f'part 2: {total}')


if __name__ == '__main__':
    main(sys.argv[1])
