#!/usr/bin/env python
import sys
from collections import defaultdict
from dataclasses import dataclass
from functools import lru_cache
from typing import List


@dataclass
class Node:
    value: int
    next: List['Node']

    def __hash__(self):
        return hash(self.value)


@dataclass
class Dag:
    start: Node
    end: Node

    @classmethod
    def from_list(cls, chain: List[int]) -> 'Dag':
        nodes = [Node(v, []) for v in chain]
        dag = cls(nodes[0], nodes[-1])
        for i in range(len(nodes)):
            for j in range(i + 1, len(nodes)):
                if nodes[j].value - nodes[i].value > 3:
                    break
                nodes[i].next.append(nodes[j])

        return dag


def parse(filename: str) -> List[int]:
    with open(filename) as f:
        return sorted(int(line) for line in f.readlines())


@lru_cache
def dfs(start: Node, end: Node) -> int:
    if start is end:
        return 1

    return sum(dfs(node, end) for node in start.next)


def main(filename: str) -> None:
    adapters = parse(filename)

    # Add outlet and device to chain
    chain = [0] + adapters + [adapters[-1] + 3]

    # Count successive difference in chain
    diff = defaultdict(int)
    for prev, curr in zip(chain[:-1], chain[1:]):
        diff[curr - prev] += 1

    # Compute puzzle output
    res = diff[1] * diff[3]
    print(f'Step 1: {res}')

    dag = Dag.from_list(chain)
    paths = dfs(dag.start, dag.end)
    print(f'Step 2: {paths}')


if __name__ == '__main__':
    main(sys.argv[1])
