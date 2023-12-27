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
        return rv, (si, sj)


lines, s_pos = read_data()
si, sj = s_pos
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


def print_lines(heads):
    for i, j in heads:
        lines[i][j] = '*'
    for i, line in enumerate(lines):
        l = []
        for j, empty in enumerate(line):
            if (i, j) in heads:
                c = '*'
            else:
                c = '_' if empty else '#'
            l.append(c)
        print(''.join(l))
    print()


def is_valid1(i, j): return 0 <= i < len_lines and 0 <= j < len_line and lines[i][j]
def is_valid2(i, j): return lines[i % len_lines][j % len_line]


def part1():
    heads = advance(64, si, sj, is_valid1)
    return len(heads)


def filter_range(heads, i0, j0, i1, j1):
    return [(i, j) for i, j in heads if i0 <= i < i1 and j0 <= j < j1]


def sq_heads_count(heads, sqi, sqj):
    return len(filter_range(heads, sqi * len_lines, sqj * len_line, (sqi + 1) * len_lines, (sqj + 1) * len_line))


def get_heads_count():
    heads = advance(65 + 131 * 4, si, sj, is_valid2)
    e_heads = sq_heads_count(heads, 0, 0)
    o_heads = sq_heads_count(heads, 0, 1)
    n_point = sq_heads_count(heads, -4, 0)
    s_point = sq_heads_count(heads, 4, 0)
    e_point = sq_heads_count(heads, 0, 4)
    w_point = sq_heads_count(heads, 0, -4)
    ne1_heads = sq_heads_count(heads, -1, 3)
    ne2_heads = sq_heads_count(heads, -2, 3)
    se1_heads = sq_heads_count(heads, 1, 3)
    se2_heads = sq_heads_count(heads, 2, 3)
    nw1_heads = sq_heads_count(heads, -1, -3)
    nw2_heads = sq_heads_count(heads, -2, -3)
    sw1_heads = sq_heads_count(heads, 1, -3)
    sw2_heads = sq_heads_count(heads, 2, -3)

    for i in range(-4, 5):
        for j in range(-4, 5):
            sq_heads = sq_heads_count(heads, i, j)
            print(str(sq_heads).ljust(5), end='')
        print()

    return (e_heads, o_heads,
            e_point, w_point, n_point, s_point,
            ne1_heads, nw1_heads, se1_heads, sw1_heads,
            ne2_heads, nw2_heads, se2_heads, sw2_heads)


def count(squares, heads_count):
    (e_heads, o_heads,
     e_point, w_point, n_point, s_point,
     ne1_heads, nw1_heads, se1_heads, sw1_heads,
     ne2_heads, nw2_heads, se2_heads, sw2_heads) = heads_count

    return (o_heads * (squares ** 2) + e_heads * ((squares - 1) ** 2) +
            e_point + w_point + n_point + s_point +
            (ne1_heads + nw1_heads + se1_heads + sw1_heads) * (squares - 1) +
            (ne2_heads + nw2_heads + se2_heads + sw2_heads) * squares)


def part2():
    # heads_count = (7424, 7436, 5601, 5585, 5574, 5612, 6501, 6497, 6524, 6512, 934, 921, 945, 939)
    heads_count = get_heads_count()
    squares = (26501365 - 65) // 131
    return count(squares, heads_count)


print('Part 1:', part1())
print('Part 2:', part2())
