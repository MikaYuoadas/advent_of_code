#!/usr/bin/env python
import re
import sys


def parse(filename):
    with open(filename) as f:
        lines = [l.split() for l in f.readlines()]
    lines.append([])

    passports = []
    current = {}
    for line in lines:
        if not line:
            passports.append(current)
            current = {}
            continue
        for field in line:
            k, v = field.split(':')
            current[k] = v

    return passports


def validate_field(f, v):
    try:
        if f == 'byr' and len(v) == 4 and 1920 <= int(v) <= 2002:
            return True
        elif f == 'iyr' and len(v) == 4 and 2010 <= int(v) <= 2020:
            return True
        elif f == 'eyr' and len(v) == 4 and 2020 <= int(v) <= 2030:
            return True
        elif f == 'hgt' and ((v[-2:] == 'cm' and 150 <= int(v[:-2]) <= 193)
                             or (v[-2:] == 'in' and 59 <= int(v[:-2]) <= 76)):
            return True
        elif f == 'hcl' and re.match(r'#[0-9a-f]{6}$', v):
            return True
        elif f == 'ecl' and v in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']:
            return True
        elif f == 'pid' and re.match(r'[0-9]{9}$', v):
            return True
    except ValueError:
        pass

    return False


def count_valid(passports, fields=['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']):
    count = 0
    for p in passports:
        for field in fields:
            try:
                value = p[field]
            except KeyError:
                break
            else:
                if not validate_field(field, value):
                    break
        else:
            count += 1

    return count


def main(filename):
    passports = parse(filename)
    print(count_valid(passports))




if __name__ == '__main__':
    main(sys.argv[1])
