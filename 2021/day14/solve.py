#!/usr/bin/env python
from argparse import ArgumentParser
from collections import Counter
from itertools import chain
from typing import Iterator


def parse(filename: str) -> tuple[str, dict[str, str]]:
    with open(filename, 'r') as f:
        polymer = f.readline().strip()
        rules = {
            rule[0]: rule[1]
            for line in f
            if len(rule := line.strip().split(' -> ')) == 2
        }

    return polymer, rules


def ipairs(polymer: str) -> Iterator[str]:
    for i in range(len(polymer) - 1):
        yield polymer[i:i+2]


def polymerize(template: str,
               rules: dict[str, str],
               steps: int = 1,
               verbose: int = 0) -> str:
    polymer = template
    if verbose:
        print(f'Template:      {template}')
    for i in range(steps):
        polymer = ''.join(
            chain(
                *zip(
                    polymer,
                    (rules[pair] for pair in ipairs(polymer))
                ),
                polymer[-1]
            )
        )
        if verbose:
            print(f'After step {i + 1:>2}: {polymer}')
    return polymer

def fast_polymerize(template: str,
                    rules: dict[str, str],
                    steps: int = 1,
                    verbose: int = 0) -> Counter[str]:
    pairs = Counter(ipairs(template))
    elements = Counter(template)
    for i in range(steps):
        new_pairs: Counter[str] = Counter()
        for pair, count in pairs.items():
            new_pairs[pair[0] + rules[pair]] += count
            new_pairs[rules[pair] + pair[1]] += count
            elements[rules[pair]] += count
        pairs = new_pairs
    return elements


def main(filename: str, verbose: int) -> None:
    template, rules = parse(filename)

    polymer = polymerize(template, rules, 10, verbose)
    most_common, *_, least_common = Counter(polymer).most_common()
    print(f'\nStep 1: {most_common[1] - least_common[1]}')

    elements = fast_polymerize(template, rules, 40, verbose)
    most_common, *_, least_common = elements.most_common()
    print(f'\nStep 2: {most_common[1] - least_common[1]}')


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('filename')
    parser.add_argument('--verbose', '-v', action='count', default=0)
    args = parser.parse_args()
    try:
        main(args.filename, args.verbose)
    except KeyboardInterrupt:
        pass
