import re
from collections import defaultdict

games = defaultdict(list)
with open('02.txt') as f:
    lines = f.readlines()
    for line in lines:
        game_id, draws = line.strip().split(': ')
        game_id = int(game_id.replace('Game ', ''))
        for draw in draws.split('; '):
            colors = ['red', 'green', 'blue']
            colors = [re.search(f'(\d+) {c}', draw) for c in colors]
            colors = [int(c.groups()[0]) if c else 0 for c in colors]
            games[game_id].append(colors)

# rv = 0
# for game_id, draws in games.items():
#     possible = True
#     for r, g, b in draws:
#         if r > 12 or g > 13 or b > 14:
#             possible = False
#             break
#     if possible:
#         rv += game_id
# print(rv)

rv = 0
for game_id, draws in games.items():
    max_colors = [0, 0, 0]
    for draw in draws:
        for i in range(3):
            max_colors[i] = max(draw[i], max_colors[i])
    rv += max_colors[0] * max_colors[1] * max_colors[2]
print(rv)
