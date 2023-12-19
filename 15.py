with open('15.txt') as f:
    seq = f.readline().strip().split(',')


def get_hash(s):
    rv = 0
    for c in s:
        rv += ord(c)
        rv *= 17
        rv %= 256
    return rv


def part1():
    return sum(get_hash(step) for step in seq)


def part2():
    boxes = [[] for _ in range(256)]

    for step in seq:
        if '=' in step:
            label, focal_length = step.split('=')
            focal_length = int(focal_length)
        else:
            label = step.replace('-', '')
            focal_length = None
        box_num = get_hash(label)
        box = boxes[box_num]
        lens_pos = [i for i, l in enumerate(box) if l[0] == label]
        print(step,'- box', box_num, end=' - ')
        assert len(lens_pos) <= 1, box
        lens_pos = lens_pos[0] if lens_pos else None

        if focal_length:
            if lens_pos is not None:
                print(f'Replacing lens "{label}" focal length {focal_length}')
                box[lens_pos][1] = focal_length
            else:
                print(f'Adding lens "{label}" focal length {focal_length}')
                box.append([label, focal_length])
        else:
            if lens_pos is not None:
                del box[lens_pos]
                print(f'Removing lens "{label}"')
            else:
                print(f'Lens "{label}" not present')
    print()
    return sum((i + 1) * (j + 1) * focal_length
               for i, box in enumerate(boxes)
               for j, (label, focal_length) in enumerate(box))


print('Part 1:', part1())
print()
print('Part 2', part2())