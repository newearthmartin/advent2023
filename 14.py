import copy


with open('14.txt') as f:
    lines1 = [list(line.strip()) for line in f.readlines()]
    lines2 = copy.deepcopy(lines1)


def move_rock(lines, i, j, direction):
    i0 = i
    j0 = j
    while True:
        i2 = i + direction[0]
        j2 = j + direction[1]
        if i2 < 0 or i2 >= len(lines): break
        if j2 < 0 or j2 >= len(lines[i]): break
        if lines[i2][j2] != '.': break
        i = i2
        j = j2
    if i0 != i or j0 != j:
        lines[i0][j0] = '.'
        lines[i][j] = 'O'


def tilt(lines, direction):
    lines_len = len(lines)
    line_len = len(lines[0])

    north_gen = ((i, j) for i in range(lines_len) for j in range(line_len))
    south_gen = ((i - 1, j) for i in range(lines_len, 0, -1) for j in range(line_len))
    west_gen = ((i, j) for j in range(line_len) for i in range(lines_len))
    east_gen = ((i, j - 1) for j in range(line_len, 0, -1) for i in range(lines_len))

    if direction == (-1, 0): gen = north_gen
    if direction == (1, 0): gen = south_gen
    if direction == (0, -1): gen = west_gen
    if direction == (0, 1): gen = east_gen
    for i, j in gen:
        if lines[i][j] == 'O': 
            move_rock(lines, i, j, direction)


def count_load(lines):
    rv = 0
    for i, line in enumerate(lines):
        rocks = sum(1 for c in line if c == 'O')
        rv += (len(lines) - i) * rocks
    return rv


def part1(lines):
    tilt(lines, (-1, 0))
    return count_load(lines)


def part2(lines):
    visited = {}
    for i in range(1000000000):
        print(i)
        state = tuple((i,j) for i, line in enumerate(lines) for j, c in enumerate(line) if c == 'O')
        if state in visited:
            cycle_start = visited[state]
            cycle_len = i - cycle_start
            break
        visited[state] = i
        tilt(lines, (-1, 0))
        tilt(lines, (0, -1))
        tilt(lines, (1, 0))
        tilt(lines, (0, 1))
    print('Cycle start', cycle_start, '- cycle length', cycle_len)

    target = (1000000000 - cycle_start) % cycle_len
    for i in range(target):
        print(1000000000 - target + i)
        tilt(lines, (-1, 0))
        tilt(lines, (0, -1))
        tilt(lines, (1, 0))
        tilt(lines, (0, 1))
    return count_load(lines)


rv1 = part1(lines1)
rv2 = part2(lines2)
print()
print('Part 1:', rv1)
print('Part 2:', rv2)
