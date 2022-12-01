#!/usr/bin/env python
import sys


def parse(filename: str) -> list[list[int]]:
    with open(filename) as f:
        inventories = []
        current: list[int] = []
        for line in f.readlines():
            try:
                current.append(int(line))
            except ValueError:
                # End of current inventory, starting next elf's
                inventories.append(current)
                current = []
        inventories.append(current)

    return inventories


def main(filename: str) -> None:
    inventories = parse(filename)

    tops = sorted((sum(inventory) for inventory in inventories), reverse=True)
    print(f"The elf carrying the most Calories has {tops[0]} Calories.")
    print("The three elf carrying the most Calories have "
          f"{tops[0]}, {tops[1]} and {tops[2]} Calories "
          f"for a total of {sum(tops[:3])} Calories.")


if __name__ == "__main__":
    main(sys.argv[1])
