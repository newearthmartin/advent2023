from functools import cache

with open('12.txt') as f:
    lines = f.readlines()
    lines = [line.strip().split(' ') for line in lines]
    lines = [(record, list(map(int, groups.split(',')))) for record, groups in lines]

for i, (record, groups) in enumerate(lines):
    lines[i] = ('?'.join([record] * 5), groups * 5)

def can_be_group(record, group, i):
    if i + group > len(record): return False
    if i != 0 and record[i-1] == '#': return False
    if any(record[i + j] == '.' for j in range(group)): return False
    return i + group == len(record) or record[i + group] in ['.', '?']        

def get_group_pos(record, group):
    group_pos = []
    for i, c in enumerate(record):
        if can_be_group(record, group, i):
            group_pos.append(i)
    return group_pos

cache = {}

def get_pos_arrangements(record, groups, group_pos, i, last_pos, path):
    cache_key = (record, groups, i, last_pos)
    if cache_key in cache: return cache[cache_key]
    if i == len(groups):
        return 1 if '#' not in record[last_pos:] else 0
    else:
        rv = 0
        group = groups[i]
        for pos in filter(lambda p: p >= last_pos, group_pos[group]):
            if '#' not in record[last_pos:pos]:
                rv += get_pos_arrangements(record, groups, group_pos, i + 1, pos + group + 1, path + [pos])
    cache[cache_key] = rv
    return rv

rv = 0
for record, groups in lines:
    print(record, groups)
    groups = tuple(groups)
    group_pos = {}
    for group in groups:
        if group not in group_pos:
            group_pos[group] = get_group_pos(record, group)
    arrangements = get_pos_arrangements(record, groups, group_pos, 0, 0, [])
    rv += arrangements
print(rv)
