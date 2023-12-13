with open('12.txt') as f:
    lines = f.readlines()
    lines = [line.strip().split(' ') for line in lines]
    lines = [(record, list(map(int, groups.split(',')))) for record, groups in lines]

def add_char(c, path, p_groups, groups):
    pos = len(p_groups) - 1
    if c == '#':
        if len(path) == 0 or path[-1] == '.':
            if len(p_groups) >= len(groups): return None
            if pos >= 0 and p_groups[pos] != groups[pos]: return None
            p_groups.append(1)
        else:
            if p_groups[pos] >= groups[pos]: return None
            p_groups[-1] += 1
    path.append(c)
    return path, p_groups

def get_arrangements(record, groups):
    paths = [([], [])]
    for c in record:
        new_paths = []
        for path, p_groups in paths:
            if c == '.' or c == '#':
                p1 = add_char(c, path, p_groups, groups)
                if p1: new_paths.append(p1)
            else:
                p1 = add_char('#', path.copy(), p_groups.copy(), groups)
                p2 = add_char('.', path, p_groups, groups)
                if p1: new_paths.append(p1)
                if p2: new_paths.append(p2)
        paths = new_paths
    return sum(1 for _, p_groups in paths if p_groups == groups)

def get_arrangements2(record, groups):
    return get_arrangements_dfs(record, groups, 0, [], [])

def get_arrangements_dfs(record, groups, i, path, p_groups):
    if i == len(record): return 1 if p_groups == groups else 0
    c = record[i]

    if c == '.' or c == '#':
        p1 = add_char(c, path, p_groups, groups)
        return get_arrangements_dfs(record, groups, i + 1, path, p_groups) if p1 else 0
    else:
        path2 = path.copy()
        p_groups2 = p_groups.copy()
        p1 = add_char('.', path, p_groups, groups)
        p2 = add_char('#', path2, p_groups2, groups)
        rv1 = get_arrangements_dfs(record, groups, i + 1, path, p_groups) if p1 else 0
        rv2 = get_arrangements_dfs(record, groups, i + 1, path2, p_groups2) if p2 else 0
        return rv1 + rv2

# for i, (record, groups) in enumerate(lines):
#     lines[i] = (record + '?') * 5, groups * 5
# lines.sort(key=lambda l: len(l[0].replace('.', '').replace('#','')))

rv = 0
for record, groups in lines:
    print(record, groups)
    rv += get_arrangements(record, groups)
    # rv += get_arrangements2(record, groups)
print(rv)
