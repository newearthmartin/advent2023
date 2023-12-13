patterns = []
pattern = []
with open('13.txt') as f:
    for line in f.readlines():
        line = line.strip()
        if line: 
            pattern.append(line)
        elif pattern:
            patterns.append(pattern)
            pattern = []
    if pattern:
        patterns.append(pattern)

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

def print_pattern(pattern):
    nums = (str((i + 1) % 10) for i in range(len(pattern[0])))
    print('  ' + ''.join(nums))
    for i, line in enumerate(pattern):
        print((i + 1) % 10, line)
    print()

rv1 = 0
rv2 = 0
for pattern in patterns:
    print_pattern(pattern)
    col1 = find_col_reflection(pattern, 0)
    row1 = find_row_reflection(pattern, 0)
    col2 = find_col_reflection(pattern, 1)
    row2 = find_row_reflection(pattern, 1)
    rv1 += col1 + row1 * 100
    rv2 += col2 + row2 * 100
    print(row1, col1, '->', rv1)
    print(row2, col2, '->', rv2)
    print()
