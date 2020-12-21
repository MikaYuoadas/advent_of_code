#!/usr/bin/env python
import re
import sys
from typing import Dict, List, Tuple


def parse(filename: str) -> Tuple[Dict[str, List[str]], List[str]]:
    with open(filename) as f:
        raw_rules, raw_msg = f.read().split('\n\n')

    rules = {key: rule.split()
             for key, rule in (line.split(':')
                               for line in raw_rules.split('\n'))}
    messages = raw_msg.strip().split('\n')

    return rules, messages


def build_regex(rules: Dict[str, List[str]], i: str = '0') -> str:
    res = []
    for c in rules[i]:
        if c.isdigit():
            res.append(build_regex(rules, c))
        elif c[0] == '"':
            res.append(c[1:-1])
        else:
            res.append(c)
    if '|' in res:
        res = ['('] + res + [')']

    return ''.join(res)


def validate(messages: List[str], pattern: str) -> List[str]:
    validator = re.compile(pattern)
    return [m for m in messages if validator.fullmatch(m)]


def main(filename: str) -> None:
    rules, messages = parse(filename)
    pattern = build_regex(rules)
    count = len(validate(messages, pattern))
    print(f'Step 1: {count}')

    rules['8'] = ['42', '*', '|']
    rules['11'] = ['42', '31', '|', '42', '11', '31']
    pattern = build_regex(rules)


if __name__ == '__main__':
    main(sys.argv[1])
