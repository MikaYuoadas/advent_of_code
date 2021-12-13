#!/usr/bin/env python
from argparse import ArgumentParser
from collections import defaultdict


def parse(filename: str) -> dict[str, set[str]]:
    graph = defaultdict(set)
    with open(filename, 'r') as f:
        for line in f:
            a, b = line.strip().split('-')
            graph[a].add(b)
            graph[b].add(a)
    return graph


def walk(
    graph: dict[str, set[str]],
    start: str,
    end: str,
    seen: set = None,
    extra_visit: bool = False,
) -> list[list[str]]:
    # We're already there
    if start == end:
        return [[end]]

    # Don't visit small cave twice
    seen = set(seen or [])
    if start.islower():
        seen.add(start)

    # Search for subpath after next move
    paths: list[list[str]] = []
    for vertex in graph[start]:
        if vertex not in seen:
            paths.extend(
                [start] + path
                for path in walk(graph, vertex, end, seen, extra_visit)
            )
        elif extra_visit and vertex != 'start':
            paths.extend(
                [start] + path
                for path in walk(graph, vertex, end, seen, False)
            )

    return paths


def main(filename: str, verbose: int) -> None:
    graph = parse(filename)

    paths = walk(graph, 'start', 'end')
    if verbose:
        for path in paths:
            print(','.join(path))
    print(f'\nStep 1: {len(paths)} paths through cave system')

    paths = walk(graph, 'start', 'end', extra_visit=True)
    if verbose:
        print()
        from collections import Counter
        for path in paths:
            print(','.join(path))
    print(f'\nStep 2: {len(paths)} paths through cave system')


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('filename')
    parser.add_argument('--verbose', '-v', action='count', default=0)
    args = parser.parse_args()
    try:
        main(args.filename, args.verbose)
    except KeyboardInterrupt:
        pass
