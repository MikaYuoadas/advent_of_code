#!/usr/bin/env python
import sys
from math import prod
from typing import List, Tuple


class Field:
    def __init__(self, name: str, ranges: List[Tuple[int, int]]):
        self.name = name
        self.ranges = ranges

    @classmethod
    def from_str(cls, value: str) -> 'Field':
        name, rest = value.split(': ')
        ranges = [tuple(map(int, range.split('-')))
                  for range in rest.split(' or ')]
        return cls(name, ranges)

    def __contains__(self, value: int) -> bool:
        if not isinstance(value, int):
            raise TypeError(f"instance of '{type(value)}' not supported")

        return any(min_ <= value <= max_ for min_, max_ in self.ranges)

    def __str__(self) -> str:
        definition = ' or '.join(f'{min_}-{max_}'
                                 for min_, max_ in self.ranges)
        return f'{self.name}: {definition}'


def parse(filename: str) -> Tuple[List[Field], List[int], List[List[int]]]:
    with open(filename) as f:
        inp = f.read().split('\n\n')

    fields = [Field.from_str(line) for line in inp[0].split('\n')]
    my_ticket = list(map(int, inp[1].split('\n')[1].split(',')))
    tickets = [list(map(int, line.split(',')))
               for line in inp[2].split('\n')[1:-1]]

    return fields, my_ticket, tickets


def validate(ticket: List[int], fields: List[Field]) -> Tuple[bool, int]:
    valid = True
    error_rate = 0
    for v in ticket:
        for field in fields:
            if v in field:
                break
        else:
            error_rate += v
            valid = False
    return valid, error_rate


def guess_fields(tickets: List[List[int]], fields: List[Field]) -> List[str]:
    order = []
    for values in zip(*tickets):
        current = set()
        for field in fields:
            if all(v in field for v in values):
                current.add(field.name)
        order.append(current)

    count = 0
    guessed = set()
    while any(len(v) > 1 for v in order):
        count += 1
        guessed.update(next(iter(names)) for names in order if len(names) == 1)
        order = [names if len(names) == 1 else names - guessed
                 for names in order]

    return [name.pop() for name in order]


def main(filename: str) -> None:
    fields, my_ticket, tickets = parse(filename)

    error_rate = 0
    for ticket in tickets:
        error_rate += validate(ticket, fields)[1]
    print(f'Step 1: {error_rate}')

    tickets = list(filter(lambda t: validate(t, fields)[0], tickets))
    field_names = guess_fields(tickets, fields)

    total = prod(my_ticket[i]
                 for i, name in enumerate(field_names)
                 if name.startswith('departure'))
    print(f'Step 2: {total}')


if __name__ == '__main__':
    main(sys.argv[1])
