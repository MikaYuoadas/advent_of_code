#!/usr/bin/env python
from argparse import ArgumentParser


LOOKUP = {
    2: {2: {2: '1'}},
    3: {2: {2: '7'}},
    4: {2: {4: '4'}},
    5: {
        1: {
            2: '2',
            3: '5',
        },
        2: {3: '3'},
    },
    6: {
        1: {3: '6'},
        2: {
            3: '0',
            4: '9',
        }
    },
    7: {2: {4: '8'}},
}


def parse(filename: str) -> list[dict[str, list[set[str]]]]:
    with open(filename) as f:
        return [
            {
                'inputs': [set(i) for i in display[0].split(' ')],
                'outputs': [set(o) for o in display[1].split(' ')],
            }
            for display in (l.strip().split(' | ') for l in f)]


def main(filename: str, verbose: int) -> None:
    notes = parse(filename)

    total = sum(len(out) in {2, 3, 4, 7}
                for note in notes
                for out in note['outputs'])
    print(f'Step 1: {total}')

    total = 0
    for note in notes:
        for pattern in note['inputs']:
            if len(pattern) == 2:
                one = pattern
            elif len(pattern) == 4:
                four = pattern
        value = int(''.join(LOOKUP[len(out)][len(one & out)][len(four & out)]
                    for out in note['outputs']))
        if verbose:
            outputs = " ".join("".join(sorted(out)) for out in note["outputs"])
            print(f'{outputs}: {value}')
        total += value
    print(f'Step 2: {total}')


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('filename')
    parser.add_argument('--verbose', '-v', action='count', default=0)
    args = parser.parse_args()
    try:
        main(args.filename, args.verbose)
    except KeyboardInterrupt:
        pass
