with open('09.txt') as f:
    lines = f.readlines()
    lines = [list(map(int, l.strip().split(' '))) for l in lines]

def get_diff_lines(line):
    diff_lines = [line.copy()]
    while not all(e == 0 for e in diff_lines[-1]):
        line_len = len(diff_lines[-1])
        diff_lines.append([0] * (line_len - 1))
        for i in range(line_len - 1):
            diff_lines[-1][i] = diff_lines[-2][i + 1] - diff_lines[-2][i]
    return list(reversed(diff_lines))

def get_next_value(line):
    diff_lines = get_diff_lines(line)
    for i, line in enumerate(diff_lines):
        if i == 0:
            line.append(0)
        else:
            line.append(line[-1] + diff_lines[i - 1][-1])
    return diff_lines[-1][-1]

def get_prev_value(line):
    diff_lines = get_diff_lines(line)
    for i, line in enumerate(diff_lines):
        if i == 0:
            line.insert(0, 0)
        else:
            line.insert(0, line[0] - diff_lines[i - 1][0])
    return diff_lines[-1][0]

rv1, rv2 = 0, 0
for line in lines:
    rv1 += get_next_value(line)
    rv2 += get_prev_value(line)
print(rv1, rv2)
