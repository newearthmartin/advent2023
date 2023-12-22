with open('21.txt') as f:
    lines = [line.strip() for line in f.readlines()]
    for i, line in enumerate(lines):
        if 'S' in line:
            si = i
            sj = line.index('S')
    len_lines = len(lines)
    len_line = len(lines[0])


def is_valid(i, j):
    return 0 <= i < len_lines and 0 <= j < len_line and lines[i][j] != '#'


def try_add(heads, i, j):
    if is_valid(i, j): heads.add((i, j))


def part1():
    heads = {(si, sj)}
    for _ in range(64):
        new_heads = set()
        for i, j in heads:
            try_add(new_heads, i + 1, j)
            try_add(new_heads, i - 1, j)
            try_add(new_heads, i, j + 1)
            try_add(new_heads, i, j - 1)
        heads = new_heads
    return len(heads)


print('Part 1:', part1())
