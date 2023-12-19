with open('10.txt') as f:
    lines = (line.strip() for line in f.readlines())
    lines = [list(line) for line in lines]


EAST = {'-', 'L', 'F'}
WEST = {'-', 'J', '7'}
NORTH = {'|', 'L', 'J'}
SOUTH = {'|', '7', 'F'}


def find_S():
    for i, line in enumerate(lines):
        try:
            j = line.index('S')
            break
        except ValueError:
            pass

    connecting_directions = [False] * 4  # LEFT, RIGHT, UP, DOWN
    connecting_pos = []

    def check(i, j, pipes, dir_index):
        if lines[i][j] in pipes:
            connecting_pos.append((i,j))
            connecting_directions[dir_index] = True

    check(i, j - 1, EAST, 0)
    check(i, j + 1, WEST, 1)
    check(i - 1, j, SOUTH, 2)
    check(i + 1, j, NORTH, 3)

    if connecting_directions[0] and connecting_directions[1]: s_tile = '-'
    if connecting_directions[0] and connecting_directions[2]: s_tile = 'J'
    if connecting_directions[0] and connecting_directions[3]: s_tile = 'J'
    if connecting_directions[1] and connecting_directions[2]: s_tile = 'L'
    if connecting_directions[1] and connecting_directions[3]: s_tile = 'F'
    if connecting_directions[2] and connecting_directions[3]: s_tile = '|'
    assert s_tile is not None
    lines[i][j] = s_tile
    return i, j, connecting_pos


def get_dir(i1, j1, i2, j2):
    di = i2 - i1
    dj = j2 - j1
    return di, dj


def get_next(i, j, direction):
    tile = lines[i][j]
    if tile == '|': return (i + 1, j) if direction == (1, 0) else (i - 1, j)
    if tile == '-': return (i, j + 1) if direction == (0, 1) else (i, j - 1)
    if tile == 'L': return (i, j + 1) if direction == (1, 0) else (i - 1, j)
    if tile == 'J': return (i, j - 1) if direction == (1, 0) else (i - 1, j)
    if tile == '7': return (i + 1, j) if direction == (0, 1) else (i, j - 1)
    if tile == 'F': return (i + 1, j) if direction == (0, -1) else (i, j + 1)
    raise Exception('should not reach this line')


def follow_path():
    si, sj, connecting_pos = find_S()
    i, j = connecting_pos[0]
    direction = get_dir(si, sj, i, j)
    path = []
    while i != si or j != sj:
        path.append((i,j))
        next_i, next_j = get_next(i, j, direction)
        direction = get_dir(i, j, next_i, next_j)
        i, j = next_i, next_j

    loop_tiles = set(path)
    loop_tiles.add((si, sj))

    for i, line in enumerate(lines):
        for j, _ in enumerate(line):
            if (i, j) not in loop_tiles:
                line[j] = '.'
        print(''.join(line))
    print()
    return path


def count_tiles():
    rv = 0
    segment_start = None
    for i, line in enumerate(lines):
        inout = False
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
        print(''.join(line))
    print()
    return rv


tile_path = follow_path()
tile_count = count_tiles()
print('Part 1:', (1 + len(tile_path)) // 2)
print('Part 2:', tile_count)