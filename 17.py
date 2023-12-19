from collections import defaultdict

with open('17.txt') as f:
    lines = (list(line.strip()) for line in f.readlines())
    lines = [list(map(int, line)) for line in lines]
    lines_len = len(lines)
    line_len = len(lines[0])


def ok(pos): return 0 <= pos[0] < lines_len and 0 <= pos[1] < line_len
def is_turn(dir1, dir2): return (dir1[0] == 0) != (dir2[0] == 0)


def print_graph(graph):
    edges = sum(1 for edges in graph.values() for edge in edges)
    print(len(graph), 'nodes -', edges, 'edges\n')


def create_graph1():
    print('creating graph - part 1')
    graph = defaultdict(list)
    dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    for i in range(lines_len):
        for j in range(line_len):
            pos = (i, j)
            for dir in dirs:
                def add_edge(n, d):
                    graph[(*pos, *dir)].append((n, d))
                if pos == (lines_len - 1, line_len - 1):
                    add_edge('end', 0)
                    continue
                if pos == (0, 0) and dir == (0, 1):
                    pos_dirs = [(1, 0), (0, 1)]
                else:
                    pos_dirs = [dir2 for dir2 in dirs if is_turn(dir, dir2)]
                for di, dj in pos_dirs:
                    dist = 0
                    ni, nj = i, j
                    for _ in range(3):
                        pos_next = ni, nj = ni + di, nj + dj
                        if not ok(pos_next): break
                        dist += lines[ni][nj]
                        add_edge((*pos_next, di, dj), dist)
    graph['start'].append(((0, 0, 0, 1), 0))
    print_graph(graph)
    return graph


def create_graph2():
    print('creating graph - part 2')
    graph = defaultdict(list)
    dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    for i in range(lines_len):
        for j in range(line_len):
            pos = (i, j)
            for dir in dirs:
                def add_edge(n, d):
                    graph[(*pos, *dir)].append((n, d))
                if pos == (lines_len - 1, line_len - 1):
                    add_edge('end', 0)
                    continue
                if pos == (0, 0) and dir == (0, 1):
                    pos_dirs = [(1, 0), (0, 1)]
                else:
                    pos_dirs = [dir2 for dir2 in dirs if is_turn(dir, dir2)]
                for di, dj in pos_dirs:
                    dist = 0
                    ni, nj = i, j
                    for step in range(10):
                        pos_next = ni, nj = ni + di, nj + dj
                        if not ok(pos_next): break
                        dist += lines[ni][nj]
                        if step >= 3:
                            add_edge((*pos_next, di, dj), dist)
    graph['start'].append(((0, 0, 0, 1), 0))
    print_graph(graph)
    return graph


def dijkstra(graph):
    edges = set(graph['start'])
    visited = {'start': 0}
    while 'end' not in visited:
        if len(visited) % 1000 == 0:
            print('visited', len(visited))
        min_dist = None
        min_next = None
        for node_next, dist in edges:
            if node_next in visited: continue
            if min_next is None or dist < min_dist:
                min_next = node_next
                min_dist = dist
        visited[min_next] = min_dist
        for n, d in graph[min_next]:
            edges.add((n, min_dist + d))
        edges = {edge for edge in edges if edge[0] not in visited}
    print('visited', len(visited))
    print('found end:', visited['end'])


dijkstra(create_graph1())
print()
dijkstra(create_graph2())