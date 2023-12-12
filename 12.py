with open('12.txt') as f:
    lines = f.readlines()
    lines = [line.strip().split(' ') for line in lines]
    lines = [(record, list(map(int, groups.split(',')))) for record, groups in lines]

def get_arrangements(record, groups):
    paths = [('', [])]
    for i, c in enumerate(record):
        new_paths = []
        for path, p_groups in paths:
            def add_char(c2):
                if c2 == '.':
                    if len(p_groups) > len(groups): return
                    pos = len(p_groups) - 1
                    if pos < 0 or groups[pos] == p_groups[pos]:
                        new_paths.append((path + c2, p_groups))
                elif c2 == '#':
                    if i == 0 or path[-1] == '.':
                        if len(p_groups) < len(groups):
                            new_paths.append((path + c2, p_groups + [1]))
                    else:
                        new_p_groups = p_groups.copy()
                        new_p_groups[-1] += 1
                        new_paths.append((path + c2, new_p_groups))
                else:
                    assert False, 'unexpected char ' + c2
            if c == '?':
                add_char('.')
                add_char('#')
            else:
                add_char(c)
        paths = new_paths
    def check_path(path):
        return path[1] == groups
    return sum(1 for _ in filter(check_path, paths))

rv = 0
for record, groups in lines:
    print(record, groups)
    rv += get_arrangements(record, groups)
print(rv)
 
