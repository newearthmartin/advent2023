with open('23.txt') as f:
    lines = [list(line.strip()) for line in f.readlines()]
    start = (0, lines[0].index('.'))
    end = (len(lines) - 1, lines[-1].index('.'))


def is_valid(pos, visited):
    ni, nj = pos
    return (0 <= ni < len(lines) and
            0 <= nj < len(lines[0]) and
            pos not in visited and
            lines[ni][nj] != '#')


def get_next(pos, visited):
    i, j = pos
    next_pos = ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1))
    return [n for n in next_pos if is_valid(n, visited)]


def part1():
    paths = [(start, {start})]
    max_tiles = {}
    while paths:
        if len(max_tiles) % 100 == 0:
            print('max len', len(max_tiles), 'and paths', len(paths))
        new_paths = []
        for pos, tiles in paths:
            if len(tiles) > len(max_tiles):
                max_tiles = tiles
            for npos in get_next(pos, tiles):
                ni, nj = npos
                new_tiles = tiles.copy()
                new_tiles.add(npos)
                nhead = npos
                c = lines[ni][nj]
                if c == '>': nhead = (ni, nj + 1)
                if c == '<': nhead = (ni, nj - 1)
                if c == 'v': nhead = (ni + 1, nj)
                if c == '^': nhead = (ni - 1, nj)
                if nhead != npos:
                    if nhead in tiles: continue
                    new_tiles.add(nhead)
                new_paths.append((nhead, new_tiles))
        paths = new_paths
    return len(max_tiles) - 1


def walk(pos, visited, steps=0):
    while True:
        visited.add(pos)
        next_pos = get_next(pos, visited)
        if len(next_pos) == 0:
            return pos, steps
        if len(next_pos) > 1:
            return pos, steps
        steps += 1
        pos = next_pos[0]


def create_graph():
    graph = {}
    nodes = [(start, get_next(start, set())), (end, get_next(end, set()))]
    for i, line in enumerate(lines):
        for j, c in enumerate(line):
            if c == '.':
                pos = (i, j)
                n_pos = get_next(pos, set())
                if len(n_pos) > 2:
                    nodes.append((pos, n_pos))
    for node, n_pos in nodes:
        graph[node] = [walk(n, {node}, steps=1) for n in n_pos]
    return graph


def part2():
    max_steps = 0
    graph = create_graph()

    def dfs(graph, node, steps, visited):
        nonlocal max_steps
        if node == end:
            if steps > max_steps:
                print('Reached new max steps', steps)
                max_steps = steps
            return
        visited.add(node)
        for next_node, next_steps in graph[node]:
            if next_node not in visited:
                dfs(graph, next_node, steps + next_steps, visited)
        visited.remove(node)

    dfs(graph, start, 0, set())
    return max_steps


print('Part 1:', part1())
print()
print('Part 2:', part2())
