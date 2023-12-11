from enum import Enum

with open('11.txt') as f:
    lines = f.readlines()
    lines = [line.strip() for line in lines]

empty_rows = set(range(len(lines)))
empty_cols = set(range(len(lines[0])))

for i, line in enumerate(lines):
    for j, c in enumerate(line):
        if c == '#':
            empty_rows.discard(i)
            empty_cols.discard(j)

galaxies = []
for i, line in enumerate(lines):
    for j, c in enumerate(line):
        if c == '#':
            galaxies.append((i, j))

def get_distance(p1, p2, increase):
    i1, j1 = p1
    i2, j2 = p2
    diff = abs(i2 - i1) + abs(j2 - j1)

    i1, i2 = sorted([i1, i2])
    j1, j2 = sorted([j1, j2])
    for r in empty_rows:
        if i1 <= r and r <= i2: 
            diff += increase
    for c in empty_cols:
        if j1 <= c and c <= j2: 
            diff += increase
    return diff

rv1 = 0
rv2 = 0
for i in range(len(galaxies)):
    for j in range(i + 1, len(galaxies)):
        p1 = galaxies[i]
        p2 = galaxies[j]
        rv1 += get_distance(p1, p2, 1)
        rv2 += get_distance(p1, p2, 999999)
print(rv1, rv2)

