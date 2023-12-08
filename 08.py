import re
import math
from functools import reduce

with open('08.txt') as f:
    instructions = f.readline().strip()
    instructions = [0 if i == 'L' else 1 for i in instructions]
    f.readline()
    nodes = f.readlines()
    nodes = map(lambda node: re.findall('\w\w\w', node), nodes)
    node_map = {n1: (n2, n3) for n1, n2, n3 in nodes}

# node = 'AAA'
# steps = 0
# while node != 'ZZZ':
#     i = steps % len(instructions)
#     node = node_map[node][instructions[i]]
#     steps += 1
# print(steps)

nodes = [n for n in node_map.keys() if n.endswith('A')]
nodes_len = len(nodes)

def get_zs(node):
    visited = {}
    steps = 0
    zs = []
    while True:
        i = steps % len(instructions)
        k = (i, node)
        if k in visited:
            break
        visited[k] = steps
        if node.endswith('Z'):
            zs.append(steps)
        node = node_map[node][instructions[i]]
        steps += 1

    cycle_start = visited[k]
    period = steps - cycle_start
    zs = [z % period for z in zs]
    return period, zs

all_zs = [get_zs(node) for node in nodes]
all_periods = [z[0] for z in all_zs]

def lcm(a, b): return abs(a*b) // math.gcd(a, b)
def lcm_multiple(numbers): return reduce(lcm, numbers)

# Since all Z positions coincide with periods, we can use LCM:

print(lcm_multiple(all_periods))