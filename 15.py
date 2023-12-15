with open('15.txt') as f:
    seq = f.readline().strip().split(',')

def hash(s):
    rv = 0
    for c in s:
        rv += ord(c)
        rv *= 17
        rv %= 256
    return rv

print('Part 1:', sum(hash(step) for step in seq))
print()

boxes = [[] for _ in range(256)]

for step in seq:
    if '=' in step:
        label, focal_length = step.split('=')
        focal_length = int(focal_length)
    else:
        label = step.replace('-', '')
        focal_length = None
    box_num = hash(label)
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

rv = 0
for i, box in enumerate(boxes):
    for j, (label, focal_length) in enumerate(box):
        rv += (i + 1) * (j + 1) * focal_length
print()
print('Part 2', rv)