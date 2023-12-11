from enum import Enum

with open('10.txt') as f:
    lines = f.readlines()
    lines = [list(line.strip()) for line in lines]

for si, line in enumerate(lines):
    try:
        sj = line.index('S')
        break
    except ValueError:
        pass

EAST = {'-', 'L', 'F'}
WEST = {'-', 'J', '7'}
NORTH = {'|', 'L', 'J'}
SOUTH = {'|', '7', 'F'}

connecting_directions = [False] * 4  # LEFT, RIGHT, UP, DOWN
connecting = []
def check(i, j, pipes, dir_index):
    if lines[i][j] in pipes: 
        connecting.append((i,j))
        connecting_directions[dir_index] = True

check(si, sj - 1, EAST, 0)
check(si, sj + 1, WEST, 1)
check(si - 1, sj, SOUTH, 2)
check(si + 1, sj, NORTH, 3)

s_tile = None
if connecting_directions[0] and connecting_directions[1]: s_tile = '-'
if connecting_directions[0] and connecting_directions[2]: s_tile = 'J'
if connecting_directions[0] and connecting_directions[3]: s_tile = 'J'
if connecting_directions[1] and connecting_directions[2]: s_tile = 'L'
if connecting_directions[1] and connecting_directions[3]: s_tile = 'F'
if connecting_directions[2] and connecting_directions[3]: s_tile = '|'
assert s_tile is not None

lines[si][sj] = s_tile

def get_dir(i1, j1, i2, j2):
    di = i2 - i1
    dj = j2 - j1
    return di, dj

def get_next(i, j, dir):
    tile = lines[i][j]
    if tile == '|': return (i + 1, j) if dir == (1, 0) else (i - 1, j)
    if tile == '-': return (i, j + 1) if dir == (0, 1) else (i, j - 1)
    if tile == 'L': return (i, j + 1) if dir == (1, 0) else (i - 1, j)
    if tile == 'J': return (i, j - 1) if dir == (1, 0) else (i - 1, j)
    if tile == '7': return (i + 1, j) if dir == (0, 1) else (i, j - 1)
    if tile == 'F': return (i + 1, j) if dir == (0, -1) else (i, j + 1)
    raise Exception('should not reach this line')

def follow(pos):
    i, j = pos
    dir = get_dir(si, sj, i, j)
    rv = []
    while i != si or j != sj:
        rv.append((i,j))
        next_i, next_j = get_next(i, j, dir)
        dir = get_dir(i, j, next_i, next_j)
        i, j = next_i, next_j
    return rv

f1 = follow(connecting[0])
f2 = follow(connecting[1])

loop_tiles = set()
loop_tiles.update(f1)
loop_tiles.add((si, sj))

for i, line in enumerate(lines):
    for j, _ in enumerate(line):
        if (i,j) not in loop_tiles:
            line[j] = '.'

rv = 0
segment_start = None
for i, line in enumerate(lines):
    inout = False
    debug = []
    for j, c in enumerate(line):
        if c == '.':
            if inout:
                rv += 1
            line[j] = 'I' if inout else 'O'
            segment_start = None
        elif c == '-':
            assert segment_start
        elif c == '|':
            inout = not inout
            segment_start = None
        elif c in ['L', 'F']:
            inout = not inout
            segment_start = c
        elif c == '7':
            assert segment_start
            if segment_start == 'F': 
                inout = not inout
            segment_start = None
        elif c == 'J':
            assert segment_start
            if segment_start == 'L':
                inout = not inout
            segment_start = None
        
        debug.append('X' if inout else ' ')
    print(''.join(line))
print(rv)