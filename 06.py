import re

with open('06.txt') as f:
    times = f.readline().replace('Time:', '')
    dists = f.readline().replace('Distance:', '')

# times = map(int, re.findall('\d+', times))
# dists = map(int, re.findall('\d+', dists))
# races = list(zip(times, dists))
# rv = 1
# for time, dist in races:
#     count = 0
#     for pressing in range(time):
#         remaining = time - pressing
#         travel = pressing * (remaining)
#         if travel > dist:
#             count += 1
#     if count > 0:
#         rv *= count
# print(rv)

time = int(''.join(re.findall('\d', times)))
dist = int(''.join(re.findall('\d', dists)))

count = 0
for pressing in range(time):
    remaining = time - pressing
    travel = pressing * (remaining)
    if travel > dist:
        count += 1
print(count)
