with open('13.txt') as f:
    lines = [line.strip() for line in f.readlines()]
    patterns = []
    current_pattern = []
    for line in lines:
        if line:
            current_pattern.append(line)
        elif current_pattern:
            patterns.append(current_pattern)
            current_pattern = []
    if current_pattern: patterns.append(current_pattern)


def rows_diff(pattern, r1, r2):
    return sum(1 for j in range(len(pattern[0])) if pattern[r1][j] != pattern[r2][j])


def cols_diff(pattern, c1, c2):
    return sum(1 for i in range(len(pattern)) if pattern[i][c1] != pattern[i][c2])


def find_row_reflection(pattern, target_count):
    rows = len(pattern)
    for i in range(rows - 1):
        diff = min(i + 1, rows - i - 1)
        count = sum(rows_diff(pattern, i - d, i + 1 + d) for d in range(diff))
        if count == target_count:
            return i + 1
    return 0


def find_col_reflection(pattern, target_count):
    cols = len(pattern[0])
    for j in range(cols - 1):
        diff = min(j + 1, cols - j - 1)
        count = sum(cols_diff(pattern, j - d, j + 1 + d) for d in range(diff))
        if count == target_count:
            return j + 1
    return 0


def count_reflections(target_count):
    col_val = sum(find_col_reflection(pattern, target_count) for pattern in patterns)
    row_val = sum(find_row_reflection(pattern, target_count) for pattern in patterns)
    return col_val + 100 * row_val


print('Part 1:', count_reflections(0))
print('Part 2:', count_reflections(1))
