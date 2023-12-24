from sympy import symbols, Eq, solve, nonlinsolve, nsolve


with open('24.txt') as f:
    lines = (line.strip().split(' @ ') for line in f.readlines())
    lines = ((p.split(', '), v.split(', ')) for p, v in lines)
    def to_ints(x): return tuple(map(int, x))
    lines = [(to_ints(p), to_ints(v)) for p, v in lines]


def intersection_point(line1, line2):  # from ChatGPT
    (x1, y1), (dx1, dy1) = line1
    (x2, y2), (dx2, dy2) = line2

    slope1 = dy1 / dx1 if dx1 != 0 else None  # Check for vertical
    slope2 = dy2 / dx2 if dx2 != 0 else None

    if slope1 is None and slope2 is None: return None  # If both lines are vertical

    if slope1 is None:  # If one line is vertical
        x_intercept = x1
        y_intercept = slope2 * (x_intercept - x2) + y2
        return x_intercept, y_intercept
    elif slope2 is None:
        x_intercept = x2
        y_intercept = slope1 * (x_intercept - x1) + y1
        return x_intercept, y_intercept

    c1 = y1 - slope1 * x1  # Calculating the y-intercepts (c = y - mx)
    c2 = y2 - slope2 * x2

    # If lines are parallel
    if slope1 == slope2: return None

    # Calculating the intersection point
    # x = (c2 - c1) / (slope1 - slope2)
    # y = slope1 * x + c1
    x_intercept = (c2 - c1) / (slope1 - slope2)
    y_intercept = slope1 * x_intercept + c1
    return x_intercept, y_intercept


def is_on_ray(intersect, start, direction):
    diff = (intersect[0] - start[0], intersect[1] - start[1])
    return (diff[0] >= 0 if direction[0] >= 0 else diff[0] <= 0) and \
           (diff[1] >= 0 if direction[1] >= 0 else diff[1] <= 0)


def cross(line1, line2):
    BOUNDARIES = (200000000000000, 400000000000000)
    p = intersection_point(line1, line2)
    if p is None: return False
    if not all(BOUNDARIES[0] <= e <= BOUNDARIES[1] for e in p): return False
    return is_on_ray(p, line1[0], line1[1]) and is_on_ray(p, line2[0], line2[1])


def part1():
    lines2d = [((x1,y1), (x2, y2)) for (x1, y1, _), (x2, y2, _) in lines]
    rv = 0
    for i, line1 in enumerate(lines2d):
        for line2 in lines2d[i+1:]:
            if cross(line1, line2):
                rv += 1
    return rv


def part2():
    print('Creating symbols')
    x, y, z, vx, vy, vz = pos_symbols = symbols('x y z vx vy vz')
    ts = symbols(' '.join(f't{i}' for i in range(len(lines))))
    print('Creating equations')
    eqs = []
    for i, ((xi, yi, zi), (vxi, vyi, vzi)) in enumerate(lines[:3]):  # it works with just 3 lines
        eqs.append(Eq(xi + vxi * ts[i], x + vx * ts[i]))
        eqs.append(Eq(yi + vyi * ts[i], y + vy * ts[i]))
        eqs.append(Eq(zi + vzi * ts[i], z + vz * ts[i]))
    print('solving')
    solution = nonlinsolve(eqs, pos_symbols + ts)
    solution = list(solution)[0]
    return solution[0] + solution[1] + solution[2]


print('Part 1:', part1())
print('Part 2:', part2())
