import re

with open('06.txt') as f:
    times = re.findall(r'\d+', f.readline())
    dists = re.findall(r'\d+', f.readline())


def count_pressings(time, dist):
    count = 0
    for pressing in range(time):
        remaining = time - pressing
        travel = pressing * (remaining)
        if travel > dist:
            count += 1
    return count


def part1():
    rv = 1
    times_int = map(int, times)
    dists_int = map(int, dists)
    for time, dist in zip(times_int, dists_int):
        count = count_pressings(time, dist)
        if count > 0:
            rv *= count
    return rv


def part2():
    time = int(''.join(times))
    dist = int(''.join(dists))
    return count_pressings(time, dist)


print('Part 1:', part1())
print('Part 2:', part2())
