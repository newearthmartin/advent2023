with open('12.txt') as f:
    lines = f.readlines()
    lines = [line.strip().split(' ') for line in lines]
    lines = [(record, list(map(int, groups.split(',')))) for record, groups in lines]

def get_arrangements(record, groups):
    paths = [([], [])]
    for i, c in enumerate(record):
        new_paths = []
        for path, p_groups in paths:
            def add_char(c2, new_path, new_p_groups):
                new_path.append(c2)
                if c2 == '.':
                    pos = len(p_groups) - 1
                    if pos < 0 or (pos < len(groups) and groups[pos] == new_p_groups[pos]): 
                        new_paths.append((new_path, new_p_groups))
                elif c2 == '#':
                    if len(new_path) == 1 or new_path[-2] == '.':
                        if len(new_p_groups) < len(groups):
                            new_p_groups.append(1)
                            new_paths.append((new_path, new_p_groups))
                    else:
                        assert len(new_p_groups) > 0
                        pos = len(p_groups) - 1
                        new_p_groups[-1] += 1
                        if new_p_groups[pos] <= groups[pos]:
                            new_paths.append((new_path, new_p_groups))
            if c == '?':
                add_char('#', path.copy(), p_groups.copy())
                add_char('.', path, p_groups)
            else:
                add_char(c, path, p_groups)
        paths = new_paths

    def check(path):
        return path[1] == groups
    return sum(1 for _ in filter(check, paths))

# for i, (record, groups) in enumerate(lines):
#     lines[i] = (record + '?') * 5, groups * 5

rv = 0
for record, groups in lines:
    print(record, groups)
    rv += get_arrangements(record, groups)
print(rv)
 
