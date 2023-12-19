with open('11.txt') as f:
    lines = [line.strip() for line in f.readlines()]
    galaxies = [(i, j) for i, line in enumerate(lines) for j, c in enumerate(line) if c == '#']
    empty_rows = set(range(len(lines)))
    empty_cols = set(range(len(lines[0])))
    for i, j in galaxies:
        empty_rows.discard(i)
        empty_cols.discard(j)


def get_distance(p1, p2, increase):
    i1, j1 = p1
    i2, j2 = p2
    diff = abs(i2 - i1) + abs(j2 - j1)

    i1, i2 = sorted([i1, i2])
    j1, j2 = sorted([j1, j2])
    for row in empty_rows:
        if i1 <= row <= i2:
            diff += increase
    for col in empty_cols:
        if j1 <= col <= j2:
            diff += increase
    return diff


def count(increase):
    rv = 0
    for i in range(len(galaxies)):
        for j in range(i + 1, len(galaxies)):
            p1 = galaxies[i]
            p2 = galaxies[j]
            rv += get_distance(p1, p2, increase)
    return rv


print('Part 1:', count(1))
print('Part 2:', count(999999))
