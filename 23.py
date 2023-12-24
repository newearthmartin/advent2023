with open('23.txt') as f:
    lines = [list(line.strip()) for line in f.readlines()]
    start = (0, lines[0].index('.'))
    end = (len(lines) - 1, lines[-1].index('.'))


def part1():
    paths = [(start, {start})]
    max_tiles = {}
    while paths:
        if len(max_tiles) % 100 == 0:
            print('max len', len(max_tiles), 'and paths', len(paths))
        new_paths = []
        for (i, j), tiles in paths:
            def try_add(ni, nj):
                npos = (ni, nj)
                if npos in tiles: return
                if ni < 0 or nj < 0 or ni >= len(lines) or nj >= len(lines[0]): return
                c = lines[ni][nj]
                if c == '#': return
                new_tiles = tiles.copy()
                new_tiles.add(npos)
                nhead = npos
                if c == '>': nhead = (ni, nj + 1)
                if c == '<': nhead = (ni, nj - 1)
                if c == 'v': nhead = (ni + 1, nj)
                if c == '^': nhead = (ni - 1, nj)
                if nhead != npos:
                    if nhead in tiles:
                        return
                    new_tiles.add(nhead)
                new_paths.append((nhead, new_tiles))

            if len(tiles) > len(max_tiles):
                max_tiles = tiles
            try_add(i + 1, j)
            try_add(i - 1, j)
            try_add(i, j + 1)
            try_add(i, j - 1)
        paths = new_paths

    for i, j in max_tiles:
        assert lines[i][j] != '#'

    return len(max_tiles) - 1


print('Part 1:', part1())
