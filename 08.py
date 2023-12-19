import re
import math
from functools import reduce

with open('08.txt') as f:
    instructions = [0 if c == 'L' else 1 for c in f.readline().strip()]
    f.readline()
    node_map = (re.findall(r'\w\w\w', line) for line in f.readlines() if line.strip())
    node_map = {n1: (n2, n3) for n1, n2, n3 in node_map}


def part1():
    node = 'AAA'
    steps = 0
    while node != 'ZZZ':
        i = steps % len(instructions)
        node = node_map[node][instructions[i]]
        steps += 1
    return steps


def lcm(a, b): return abs(a*b) // math.gcd(a, b)
def lcm_multiple(numbers): return reduce(lcm, numbers)


def part2():
    nodes = [n for n in node_map.keys() if n.endswith('A')]

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

    return lcm_multiple(all_periods)  # Since all Z positions coincide with periods, we can use LCM


print('Part 1:', part1())
print('Part 2:', part2())