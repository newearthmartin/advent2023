with open('18.txt') as f:
    lines = [line.strip().split(' ') for line in f.readlines() if line.strip()]
    lines = [(direction, int(num), color[2:-1]) for direction, num, color in lines]

min_i, max_i = None, None
min_j, max_j = None, None


def get_plan():
    plan = {(0, 0): True}
    i = 0
    j = 0
    for direction, num, _ in lines:
        def paint(incr_i, incr_j):
            nonlocal i, j
            global max_i, max_j, min_i, min_j
            for _ in range(num):
                i += incr_i
                j += incr_j
                plan[(i,j)] = direction
            max_i = max(max_i, i) if max_i is not None else i
            max_j = max(max_j, j) if max_j is not None else j
            min_i = min(min_i, i) if min_i is not None else i
            min_j = min(min_j, j) if min_j is not None else j
        if direction == 'U':
            plan[(i, j)] = 'U'
            paint(-1, 0)
        if direction == 'D':
            plan[(i, j)] = 'D'
            paint(1, 0)
        if direction == 'L': paint(0, -1)
        if direction == 'R': paint(0, 1)
    return plan


def count(plan):
    rv = 0
    for i in range(min_i, max_i + 1):
        inout = False
        start = None

        l = []
        for j in range(min_j - 1, max_j + 2):
            if (i, j) in plan:
                direction = plan[(i, j)]
                rv += 1
                if direction in ['L', 'R']:
                    pass
                elif direction in ['U', 'D']:
                    if start:
                        if direction != start:
                            inout = not inout
                        start = None
                    else:
                        inout = not inout
                        start = direction
                l.append(direction)
            else:
                start = None
                if inout:
                    rv += 1
                    l.append('#')
                else:
                    l.append(' ')
        # print(''.join(l))
    return rv


print('Part 1:', count(get_plan()))
