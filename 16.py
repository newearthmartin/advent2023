with open('16.txt') as f:
    lines = [line.strip() for line in f.readlines() if line.strip()]


def energize_tiles(pos, dir):
    heads = [(pos, dir)]
    visited = set()
    visited_tiles = set()
    while heads:
        new_heads = []
        for head in heads:
            if head in visited: continue
            ((i,j), (diri, dirj)) = (pos, dir) = head
            visited.add(head)
            visited_tiles.add(pos)
            c = lines[i][j]
            if c == '.': dirs = [dir]
            if c == '/':
                if dir == (1, 0): dirs = [(0, -1)]
                if dir == (-1, 0): dirs = [(0, 1)]
                if dir == (0, 1): dirs = [(-1, 0)]
                if dir == (0, -1): dirs = [(1, 0)]
            if c == '\\':
                if dir == (1, 0): dirs = [(0, 1)]
                if dir == (-1, 0): dirs = [(0, -1)]
                if dir == (0, 1): dirs = [(1, 0)]
                if dir == (0, -1): dirs = [(-1, 0)]
            if c == '-':
                if diri == 0: dirs = [dir]
                else: dirs = [(0, 1), (0, -1)]
            if c == '|':
                if dirj == 0: dirs = [dir]
                else: dirs = [(1, 0), (-1, 0)]
            assert dirs
            for dir2 in dirs:
                dir2i, dir2j = dir2
                pos2 = (i2, j2) = (i + dir2i, j + dir2j)
                if i2 < 0 or i2 >= len(lines) or j2 < 0 or j2 >= len(lines[0]):  continue
                new_heads.append((pos2, dir2))
        heads = new_heads
    return len(visited_tiles)

print('Part 1', energize_tiles((0, 0), (0, 1)))

line_len = len(lines[0])
max_tiles = 0
for i in range(len(lines)):
    max_tiles = max(max_tiles, energize_tiles((i, 0), (0, 1)))
    max_tiles = max(max_tiles, energize_tiles((i, line_len - 1), (0, -1)))
for j in range(line_len):
    max_tiles = max(max_tiles, energize_tiles((0, j), (1, 0)))
    max_tiles = max(max_tiles, energize_tiles((len(lines) - 1, j), (-1, 0)))
print('Part 2', max_tiles)