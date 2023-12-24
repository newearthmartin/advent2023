from copy import deepcopy

with open('22.txt') as f:
    lines = (line.strip().split('~') for line in f.readlines())
    lines = ((v1.split(','), v2.split(',')) for v1, v2 in lines)
    lines = [(list(map(int, v1)), list(map(int, v2))) for v1, v2 in lines]
    lines = sorted(lines, key=lambda l: (l[0][2], l[1][2]))

top_x = 0
top_y = 0
top_z = 0
for v1, v2 in lines:
    assert v1[2] <= v2[2]
    top_x = max(top_x, v2[0])
    top_y = max(top_y, v2[1])
    top_z = max(top_z, v2[2])


def find_resting(bricks, space, brick_i):
    brick = bricks[brick_i]
    (x1, y1, z1), (x2, y2, z2) = b1, b2 = brick
    xlen = x2 - x1 + 1
    ylen = y2 - y1 + 1
    zlen = z2 - z1 + 1
    support = set()
    if z1 != 1:
        for new_z in range(z1, 0, -1):
            if new_z == 1 or any((x1 + dx, y1 + dy, new_z - 1) in space for dx in range(xlen) for dy in range(ylen)):
                break
        b1[2] = new_z
        b2[2] = new_z + zlen - 1
        (x1, y1, z1), (x2, y2, z2) = b1, b2
        if new_z > 1:
            for dx in range(xlen):
                for dy in range(ylen):
                    space_pos = space.get((x1 + dx, y1 + dy, z1 - 1), None)
                    if space_pos is not None:
                        support.add(space_pos)
    support = list(support)

    for dx in range(xlen):
        for dy in range(ylen):
            for dz in range(zlen):
                key = (x1 + dx, y1 + dy, z1 + dz)
                assert key not in space, f'brick {brick_i} conflicts with brick {space.get(key, None)}'
                space[key] = brick_i
    return support


def fall(bricks):
    space = {}
    rests_on = {}
    for i in range(len(bricks)):
        rests_on[i] = find_resting(bricks, space, i)
    return space, rests_on


def part1(bricks):
    space, rests_on = fall(bricks)
    essential = {rests_on[i][0] for i in range(len(bricks)) if len(rests_on[i]) == 1}
    return len(bricks) - len(essential)


def delete_and_test(bricks0, i):
    bricks1 = deepcopy(bricks0)
    del bricks1[i]
    fall(bricks1)
    return sum(1 for j in range(len(bricks1)) if bricks1[j] != bricks0[j if j < i else (j + 1)])


def part2(bricks):
    fall(bricks)
    return sum(delete_and_test(bricks, i) for i in range(len(bricks)))


print('Part 1:', part1(lines.copy()))
print('Part 2:', part2(lines))
