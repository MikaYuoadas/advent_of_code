#!/usr/bin/env python
from argparse import ArgumentParser
from functools import reduce


SCORE_TABLE = {
    'error': {
        ')': 3,
        ']': 57,
        '}': 1197,
        '>': 25137,
    },
    'complete': {
        ')': 1,
        ']': 2,
        '}': 3,
        '>': 4,
    },
}


class SyntaxChecker:
    pairs = {
        '(': ')',
        '[': ']',
        '{': '}',
        '<': '>',
    }

    def __init__(self, filename: str) -> None:
        self.filename = filename
        with open(filename, 'r') as f:
            self.lines = f.read().splitlines()

    def autocomplete(self, line: int) -> str:
        waiting = []
        for offset, c in enumerate(self.lines[line]):
            if c in self.pairs:
                waiting.append(self.pairs[c])
            else:
                try:
                    expected = waiting.pop()
                except IndexError:
                    raise SyntaxError(
                        f'Unexpected character {c}!',
                        (
                            self.filename,
                            line,
                            offset + 1,
                            self.lines[line],
                        ),
                    )
                if c != expected:
                    raise SyntaxError(
                        f'Expected {expected}, but found {c} instead!',
                        (
                            self.filename,
                            line,
                            offset + 1,
                            self.lines[line],
                        ),
                    )
        return ''.join(reversed(waiting))


def main(filename: str, verbose: int) -> None:
    checker = SyntaxChecker(filename)

    error_score = 0
    scores = []
    for line in range(len(checker.lines)):
        try:
            completion = checker.autocomplete(line)
        except SyntaxError as e:
            error_score += SCORE_TABLE['error'][e.text[e.offset - 1]]
            if verbose >= 2:
                print(e.text)
                print(f'{"^":>{e.offset}}')
                print(f'Error line {line + 1}: {e.msg}')
                print()
            elif verbose:
                print(f'Error line {line + 1}: {e.msg}')
        else:
            scores.append(reduce(
                lambda total, new: total * 5 + new,
                (SCORE_TABLE['complete'][c] for c in completion),
            ))
            if verbose:
                print(f'Completion line {line + 1}: {completion}')
                if verbose >= 2:
                    print()
    score = sorted(scores)[len(scores) // 2]

    print(f'\nStep 1: syntax error score: {error_score}')
    print(f'Step 2: autocomplete score: {score}')


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('filename')
    parser.add_argument('--verbose', '-v', action='count', default=0)
    args = parser.parse_args()
    try:
        main(args.filename, args.verbose)
    except KeyboardInterrupt:
        pass
