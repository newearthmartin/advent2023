import json


def read_data():
    with (open('21.txt') as f):
        rv = [list(line.strip()) for line in f.readlines()]
        for i, line in enumerate(rv):
            if 'S' in line:
                si = i
                sj = line.index('S')
        for line in rv:
            for j, c in enumerate(line):
                line[j] = c != '#'
        return rv, si, sj


lines, si, sj = read_data()
s_pos = si, sj
len_lines = len(lines)
len_line = len(lines[0])


def advance(times, i, j, valid_func):
    heads = {(i, j)}
    for _ in range(times):
        new_heads = set()

        def try_add(i, j):
            if valid_func(i, j): new_heads.add((i, j))

        for i, j in heads:
            try_add(i + 1, j)
            try_add(i - 1, j)
            try_add(i, j + 1)
            try_add(i, j - 1)
        heads = new_heads
    return heads


def part1():
    def is_valid(i, j):
        return 0 <= i < len_lines and 0 <= j < len_line and lines[i][j]
    heads = advance(64, si, sj, is_valid)
    return len(heads)


def add_caches(heads_cache, curr, prev1, prev2):
    print('Growing cache', curr, f'as {prev1} + {prev2}')
    heads_cache[curr] = {}
    for pos, heads in heads_cache[prev1].items():
        pi, pj = pos
        heads_cache[curr][pos] = {(hi + hi2, hj + hj2)
                                  for hi, hj in heads
                                  for hi2, hj2 in heads_cache[prev2][((pi + hi) % len_lines, (pj + hj)% len_line)]}


def get_cache(heads_cache, level, is_valid, prev1=None):
    if level in heads_cache:
        print('Already cached', level)
        return
    print('Creating cache', level)
    if level == 1:
        heads_cache[1] = {}
        for i in range(len_lines):
            for j in range(len_line):
                heads = advance(1, i, j, is_valid)
                heads_cache[1][(i, j)] = {(hi - i, hj - j) for hi, hj in heads}
    else:
        if not prev1:
            prev1 = level // 2
        add_caches(heads_cache, level, prev1, level - prev1)
    print('writing caches file')
    write_heads_cache(heads_cache)


def grow_heads_cache(times, is_valid):
    heads_cache = read_heads_cache()
    for l in range(times):
        get_cache(heads_cache, 2 ** l, is_valid)
    return heads_cache


def write_heads_cache(heads_cache):
    with open('21.cache.txt', 'w') as out:
        for level, cache in heads_cache.items():
            out_cache = {f'{k[0]},{k[1]}': [list(pos) for pos in v] for k, v in cache.items()}
            out_cache = json.dumps(out_cache).replace(' ', '')
            out.write(f"{level}: {out_cache}\n")


def read_heads_cache():
    heads_cache = {}
    print('Loading caches file')
    try:
        with open('21.cache.txt') as f:
            lines = [line.strip() for line in f.readlines()]
    except FileNotFoundError:
        return heads_cache
    for line in lines:
        level, cache = line.split(': ', maxsplit=1)
        level = int(level.strip())
        cache = json.loads(cache.strip())
        cache = {tuple(map(int, k.split(','))): [tuple(pos) for pos in v] for k, v in cache.items()}
        heads_cache[level] = cache
    return heads_cache


def part2():
    def is_valid(i, j):
        return lines[i % len_lines][j % len_line] is True

    cache_heads = grow_heads_cache(24, is_valid)
    exit(0)

    cycle_len = max(len_lines, len_line)
    first_steps = 26501365 % cycle_len
    cycles = (26501365 - first_steps) // cycle_len
    heads_cache = get_heads_cache(cycle_len, is_valid)
    # heads_cache = read_heads_cache()

    print(f'First {first_steps} steps')
    heads = advance(first_steps, si, sj, is_valid)

    print('Starting cycles')
    for step in range(cycles):
        print(step, len(heads))
        new_heads = set()
        for hi, hj in heads:
            new_heads.update((hi + i, hj + j) for i, j in heads_cache[(hi % len_lines, hj % len_line)])
        heads = new_heads
    return len(heads)


# print('Part 1:', part1())
print('Part 2:', part2())
