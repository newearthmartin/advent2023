from collections import defaultdict
from igraph import Graph


with (open('25.txt') as f):
    lines = (line.strip().split(': ') for line in f.readlines())
    wires = {cmp1: cmps.split(' ') for cmp1, cmps in lines}
    edges = [(cmp1, cmp2) for cmp1, cmps in wires.items() for cmp2 in cmps]
    wires2 = defaultdict(set)
    for n1, n2 in edges:
        wires2[n1].add(n2)
        wires2[n2].add(n1)
    components = list(wires2.keys())
    components.sort()


def part1():
    g = Graph()
    g.add_vertices(components)
    g.add_edges(edges)
    min_cut = g.mincut()
    return len(min_cut.partition[0]) * len(min_cut.partition[1])


print('Part 1:', part1())
