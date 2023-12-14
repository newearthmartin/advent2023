with open('14.txt') as f:
    lines = [list(l.strip()) for l in f.readlines()]

def move_rock(i, j, dir):
    i0 = i
    j0 = j
    while True:
        i2 = i + dir[0]
        j2 = j + dir[1]
        if i2 < 0 or i2 >= len(lines): break
        if j2 < 0 or j2 >= len(lines[i]): break
        if lines[i2][j2] != '.': break
        i = i2
        j = j2
    if i0 != i or j0 != j:
        lines[i0][j0] = '.'
        lines[i][j] = 'O'

def tilt(dir):
    lines_len = len(lines)
    line_len = len(lines[0])
    def north_generator():
        for i in range(lines_len): 
            for j in range(line_len): 
                yield(i,j)
    def south_generator():
        for i in range(lines_len, 0, -1):
            for j in range(line_len):
                yield(i - 1, j)
    def west_generator():
        for j in range(line_len):
            for i in range(lines_len):
                yield(i, j)
    def east_generator():
        for j in range(line_len, 0, -1):
            for i in range(lines_len):
                yield(i, j - 1)
    if dir == (-1, 0): gen = north_generator
    if dir == (1, 0): gen = south_generator
    if dir == (0, -1): gen = west_generator
    if dir == (0, 1): gen = east_generator
    for i, j in gen():
        if lines[i][j] == 'O': 
            move_rock(i, j, dir)

# tilt((-1, 0))

visited = {}
for i in range(1000000000):
    print(i)
    state = tuple((i,j) for i, line in enumerate(lines) for j, c in enumerate(line) if c == 'O')
    if state in visited:
        cycle_start = visited[state]
        cycle_len = i - cycle_start
        break
    visited[state] = i
    tilt((-1, 0))
    tilt((0, -1))
    tilt((1, 0))
    tilt((0, 1))
print('Cycle start', cycle_start, '- cycle length', cycle_len)

target = (1000000000 - cycle_start) % cycle_len
for i in range(target):
    print(1000000000 - target + i)
    tilt((-1, 0))
    tilt((0, -1))
    tilt((1, 0))
    tilt((0, 1))

rv = 0
for i, line in enumerate(lines):
    rocks = sum(1 for c in line if c == 'O')
    rv += (len(lines) - i) * rocks
print('Weight', rv)
