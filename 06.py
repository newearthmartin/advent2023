import re

with open('06.txt') as f:
    times = f.readline().replace('Time:', '')
    dists = f.readline().replace('Distance:', '')
    times = re.findall('\d+', times)
    dists = re.findall('\d+', dists)

def count_pressings(time, dist):
    count = 0
    for pressing in range(time):
        remaining = time - pressing
        travel = pressing * (remaining)
        if travel > dist:
            count += 1
    return count

times = map(int, times)
dists = map(int, dists)
races = list(zip(times, dists))
rv = 1
for time, dist in races:
    count = count_pressings(time, dist)
    if count > 0:
        rv *= count
print(rv)

# time = int(''.join(times))
# dist = int(''.join(dists))
# count = count_pressings(time, dist)
# print(count)
