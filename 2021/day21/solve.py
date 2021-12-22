#!/usr/bin/env python
import re
from argparse import ArgumentParser
from collections import Counter
from collections.abc import Iterator, Sequence
from itertools import cycle, islice, product, repeat
from operator import attrgetter
from typing import NamedTuple


def parse(filename: str) -> list[int]:
    with open(filename, 'r') as f:
        return [
            int(m[1])
            for line in f
            if (m := re.match(r'Player \d+ starting position: (\d+)', line))
        ]


class DiracDice:
    def __init__(
        self,
        starting_positions: list[int],
        dice: Iterator[int],
        verbose: int = 0,
    ) -> None:
        if len(starting_positions) != 2:
            raise ValueError('It\'s a 2 players game!')
        self.positions = [starting_positions[0] - 1, starting_positions[1] - 1]
        self.dice_rolls = 0
        self.scores = [0, 0]
        self.player = 0
        self.dice = dice
        self.verbose = verbose

    @property
    def won(self) -> bool:
        return max(*self.scores) >= 1000

    def _rolls(self, n: int = 1) -> list[int]:
        self.dice_rolls += n
        return list(islice(self.dice, n))

    def turn(self) -> None:
        rolls = self._rolls(3)

        # Update board
        self.positions[self.player] += sum(rolls)
        self.positions[self.player] %= 10
        self.scores[self.player] += self.positions[self.player] + 1

        if self.verbose:
            print(
                f'Player {self.player + 1} '
                f'rolls {"+".join(str(r) for r in rolls)} '
                f'and moves to space {self.positions[self.player] + 1} '
                f'for a total score of {self.scores[self.player]}.'
            )

        # Change player turn
        self.player = not self.player


class Universe(NamedTuple):
    positions: tuple[int, int]
    scores: tuple[int, int]
    won: bool

    def __repr__(self):
        return f'[{self.positions}, {self.scores}]'


class QuantumDiracDice:
    def __init__(
        self,
        starting_positions: list[int],
        dice: Iterator[Sequence[int]],
        goal: int,
    ) -> None:
        if len(starting_positions) != 2:
            raise ValueError('It\'s a 2 players game!')
        self.dice = dice
        self.goal = goal
        self.player = 0
        self.universes: Counter[Universe] = Counter()
        self.universes[Universe(
            (starting_positions[0] - 1, starting_positions[1] - 1),
            (0, 0),
            False,
        )] = 1

    @property
    def universes_won(self) -> tuple[int, int]:
        return (
            sum(map(
                lambda x: x[0].scores[0] >= self.goal and x[1],
                self.universes.items(),
            )),
            sum(map(
                lambda x: x[0].scores[1] >= self.goal and x[1],
                self.universes.items(),
            )),
        )

    @property
    def won(self) -> bool:
        return all(map(attrgetter('won'), self.universes))

    def _rolls(self, n: int = 1) -> Counter[int]:
        return Counter(map(sum, product(*islice(self.dice, 3))))

    def turn(self) -> None:
        rolls = self._rolls(3)

        universes: Counter[Universe] = Counter()
        for u, ucount in self.universes.items():
            if u.won:
                # These timeline have already ended
                universes[u] += ucount
                continue

            # Split current universe for each possible roll
            for roll, rcount in rolls.items():
                positions = list(u.positions)
                scores = list(u.scores)

                # Update board with current roll possibility
                positions[self.player] += roll
                positions[self.player] %= 10
                scores[self.player] += positions[self.player] + 1

                # Create the resulting universes
                universe = Universe(
                    (positions[0], positions[1]),
                    (scores[0], scores[1]),
                    max(scores) >= self.goal,
                )
                universes[universe] += ucount * rcount

        self.universes = universes

        # Change player turn
        self.player = not self.player


def main(filename: str, verbose: int) -> None:
    starting_positions = parse(filename)

    dice = cycle(range(1, 101))
    game = DiracDice(starting_positions, dice, verbose)
    while not game.won:
        game.turn()
    result = game.dice_rolls * min(*game.scores)
    print(f'\nStep 1: {result}')

    qdice = repeat((1, 2, 3))
    qgame = QuantumDiracDice(starting_positions, qdice, 21)
    i = 0
    while not qgame.won:
        i += 1
        if verbose:
            print(f'\nturn {i}')
            print(f'    {sum(qgame.universes.values())} total universes')
            print(f'    ({len(qgame.universes)} distincts)')
            print(f'    player 1 won in {qgame.universes_won[0]} universes')
            print(f'    player 2 won in {qgame.universes_won[1]} universes')
        qgame.turn()

    print(f'\nStep 2: best player won in {max(*qgame.universes_won)} universes')


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('filename')
    parser.add_argument('--verbose', '-v', action='count', default=0)
    args = parser.parse_args()
    try:
        main(args.filename, args.verbose)
    except KeyboardInterrupt:
        pass
