#!/usr/bin/env python
import sys


class Interpreter:
    def __init__(self):
        self.code = []
        self.reset()

    def reset(self):
        self.ptr = 0
        self.acc = 0
        self.lines_executed = set()

    def load(self, code):
        self.code = code

    def run(self):
        self.reset()
        while self.ptr < len(self.code):
            current, offset = self.code[self.ptr]
            if self.ptr in self.lines_executed:
                raise RuntimeError('Infinite loop')
            else:
                self.lines_executed.add(self.ptr)

            self.ptr += 1
            if current == 'nop':
                pass
            elif current == 'acc':
                self.acc += offset
            elif current == 'jmp':
                self.ptr += offset - 1
            else:
                raise ValueError(f'Unknown instruction: {current}')
        return self.acc


def parse(filename):
    code = []
    with open(filename) as f:
        for line in f.readlines():
            i, n = line.split()
            n = int(n)
            code.append((i, n))
    return code


def fix_and_run(code, interpreter):
    for i, (inst, offset) in enumerate(code):
        fixed_code = list(code)
        if inst == 'nop':
            fixed_code[i] = ('jmp', offset)
        elif inst == 'jmp':
            fixed_code[i] = ('nop', offset)
        else:
            continue

        interpreter.load(fixed_code)
        try:
            acc = interpreter.run()
        except RuntimeError:
            continue
        else:
            return acc


def main(filename):
    interpreter = Interpreter()
    code = parse(filename)
    interpreter.load(code)

    try:
        interpreter.run()
    except RuntimeError:
        print(f'Step 1: {interpreter.acc}')

    acc = fix_and_run(code, interpreter)
    print(f'Step 2: {acc}')



if __name__ == '__main__':
    main(sys.argv[1])
