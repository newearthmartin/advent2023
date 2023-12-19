import re

with open('03.txt') as f:
    lines = [line.strip() for line in f.readlines()]

symbols = []
numbers = []
for i, line in enumerate(lines):
    numbers += [(i, m.span()[0], m.group()) for m in re.finditer(r'\d+', line)]
    symbols += [(i, j, c) for j, c in enumerate(line) if not c.isdigit() and c != '.']


def touches(ni, nj, num, si, sj):
    return abs(ni - si) <= 1 and nj - 1 <= sj <= nj + len(num)


def part1():
    return sum(int(num) for ni, nj, num in numbers
               if any(touches(ni, nj, num, si, sj) for si, sj, _ in symbols))


def part2():
    gears = [(si, sj) for si, sj, sym in symbols if sym == '*']
    touched = [
        [num for ni, nj, num in numbers if touches(ni, nj, num, si, sj)]
        for si, sj in gears
    ]
    parts = [p for p in touched if len(p) == 2]
    return sum(int(p1) * int(p2) for p1, p2 in parts)


print('Part 1:', part1())
print('Part 2:', part2())
