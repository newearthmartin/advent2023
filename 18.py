with open('18.txt') as f:
    lines = (line.strip() for line in f.readlines())
    lines = (line.split(' ') for line in lines if line)
    lines = [(direction, int(num), color[2:-1]) for direction, num, color in lines]


def get_min_max():
    i, j = 0, 0
    min_i, min_j, max_i, max_j = 0, 0, 0, 0
    for direction, num, _ in lines:
        if direction == 'U': i -= num
        if direction == 'D': i += num
        if direction == 'L': j -= num
        if direction == 'R': j += num
        max_i = max(max_i, i)
        max_j = max(max_j, j)
        min_i = min(min_i, i)
        min_j = min(min_j, j)
    return min_i, min_j, max_i, max_j


def get_plan():
    min_i, min_j, max_i, max_j = get_min_max()
    print('creating plan', max_i - min_i, 'rows', max_j - min_j, 'cols')
    print('initializing')
    plan = [None] * (max_i - min_i + 1)
    for i in range(len(plan)):
        plan[i] = []
    i, j = 0, 0
    print('painting')
    for direction, num, _ in lines:
        if direction in ['U', 'D']:
            incr = 1 if direction == 'D' else -1
            plan[i - min_i].append((j, 1, direction))
            for _ in range(num):
                i += incr
                plan[i - min_i].append((j, 1, direction))
        else:
            start = (j + 1) if direction == 'R' else (j - num + 1)
            plan[i - min_i].append((start, num - 1, direction))
            if direction == 'R':
                j += num
            else:
                j -= num
    print('sorting')
    for line in plan:
        line.sort(key=lambda e: e[0])
    return plan


def count(plan):
    print('counting: ', end='')
    rv = 0
    for segments in plan:
        inout = False
        start = None
        last_j = None
        for j, length, direction in segments:
            if last_j is not None:
                assert last_j <= j
                if last_j < j: start = None
                if inout: rv += j - last_j
            last_j = j + length
            rv += length
            if direction in ['U', 'D']:
                if start:
                    if direction != start:
                        inout = not inout
                    start = None
                else:
                    inout = not inout
                    start = direction
    print(rv)


def reinterpret():
    for i, line in enumerate(lines):
        direction, num, color = line
        direction = color[-1]
        if direction == '0': direction = 'R'
        if direction == '1': direction = 'D'
        if direction == '2': direction = 'L'
        if direction == '3': direction = 'U'
        num = int(color[0:5], base=16)
        lines[i] = (direction, num, color)


print('Part 1\n')
count(get_plan())
print()

print('Part 2\n')
reinterpret()
count(get_plan())

