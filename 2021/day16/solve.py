#!/usr/bin/env python
from argparse import ArgumentParser
from dataclasses import dataclass
from math import prod
from pathlib import Path
from typing import Optional, Type


def parse(filename: str) -> str:
    with open(filename, 'r') as f:
        return ''.join(format(b, '08b')
                       for b in bytes.fromhex(f.read().strip()))


@dataclass
class Packet:
    version: int
    type_id: int

    @property
    def cumulated_version(self) -> int:
        return self.version

    @classmethod
    def frombits(cls, bits: str) -> 'Packet':
        return cls._frombits(bits)[0]

    @classmethod
    def _frombits(cls, bits: str) -> tuple['Packet', str]:
        version = int(bits[0:3], 2)
        type_id = int(bits[3:6], 2)
        if type_id == 4:
            value, remaining = LiteralPacket.get_value(bits[6:])
            return LiteralPacket(version, type_id, value), remaining
        else:
            length_type_id = int(bits[6], 2)
            if length_type_id:
                length = int(bits[7:18], 2)
                packets, remaining = OperatorPacket.get_packets(bits[18:],
                                                                n=length)
            else:
                length = int(bits[7:22], 2)
                packets, _ = OperatorPacket.get_packets(
                    bits[22:22 + length]
                )
                remaining = bits[22 + length:]
            return OperatorPacket.cls_from_type_id(type_id)(
                version,
                type_id,
                length_type_id,
                length,
                packets,
            ), remaining


@dataclass
class LiteralPacket(Packet):
    value: int

    @staticmethod
    def get_value(bits: str) -> tuple[int, str]:
        value = 0
        for i in range(0, len(bits), 5):
            quintet = bits[i:i+5]
            value = (value << 4) + (int(quintet[1:], 2) & 0xf)
            if quintet[0] != '1':
                break
        return value, bits[i+5:]

    def __str__(self) -> str:
        return str(self.value)


@dataclass
class OperatorPacket(Packet):
    length_type_id: int
    length: int
    packets: list[Packet]

    @staticmethod
    def cls_from_type_id(type_id: int) -> Type['OperatorPacket']:
        match type_id:
            case 0:
                return SumPacket
            case 1:
                return ProdPacket
            case 2:
                return MinPacket
            case 3:
                return MaxPacket
            case 5:
                return GtPacket
            case 6:
                return LtPacket
            case 7:
                return EqPacket

    @property
    def cumulated_version(self) -> int:
        return super().cumulated_version + sum(p.cumulated_version
                                               for p in self.packets)

    @classmethod
    def get_packets(
        cls,
        bits: str,
        n: int = 2 ** 64,
    ) -> tuple[list[Packet], str]:
        packets = []
        for _ in range(n):
            p, bits = cls._frombits(bits)
            packets.append(p)
            if not bits:
                break
        return packets, bits


class SumPacket(OperatorPacket):
    @property
    def value(self) -> int:
        return sum(p.value for p in self.packets)

    def __str__(self) -> str:
        return f'({" + ".join(map(str, self.packets))})'


class ProdPacket(OperatorPacket):
    @property
    def value(self) -> int:
        return prod(p.value for p in self.packets)

    def __str__(self) -> str:
        return f'({" * ".join(map(str, self.packets))})'


class MinPacket(OperatorPacket):
    @property
    def value(self) -> int:
        return min(p.value for p in self.packets)

    def __str__(self) -> str:
        return f'min({", ".join(map(str, self.packets))})'


class MaxPacket(OperatorPacket):
    @property
    def value(self) -> int:
        return max(p.value for p in self.packets)

    def __str__(self) -> str:
        return f'max({", ".join(map(str, self.packets))})'


class GtPacket(OperatorPacket):
    @property
    def value(self) -> int:
        return int(self.packets[0].value > self.packets[1].value)

    def __str__(self) -> str:
        return f'({self.packets[0]} > {self.packets[1]})'


class LtPacket(OperatorPacket):
    @property
    def value(self) -> int:
        return int(self.packets[0].value < self.packets[1].value)

    def __str__(self) -> str:
        return f'({self.packets[0]} < {self.packets[1]})'


class EqPacket(OperatorPacket):
    @property
    def value(self) -> int:
        return int(self.packets[0].value == self.packets[1].value)

    def __str__(self) -> str:
        return f'({self.packets[0]} = {self.packets[1]})'


def main(filename: str, verbose: int) -> None:
    if Path(filename).exists():
        bits = parse(filename)
    else:
        bits = ''.join(format(b, '08b')
                       for b in bytes.fromhex(filename))

    packet = Packet.frombits(bits)
    if verbose:
        print(packet)
    print(f'\nStep 1: sum of versions: {packet.cumulated_version}')
    print(f'\nStep 2: value of transmission: {packet.value}')


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('filename')
    parser.add_argument('--verbose', '-v', action='count', default=0)
    args = parser.parse_args()
    try:
        main(args.filename, args.verbose)
    except KeyboardInterrupt:
        pass
