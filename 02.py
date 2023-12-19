import re

COLORS = ['red', 'green', 'blue']

with open('02.txt') as f:
    lines = f.readlines()
    lines = (line.strip().split(': ') for line in lines)
    lines = ((int(game_id.replace('Game ', '')), draws) for game_id, draws in lines)

    def parse(draw):
        colors = [re.search(f'(\\d+) {c}', draw) for c in COLORS]
        return [int(c.groups()[0]) if c else 0 for c in colors]
    lines = [(game_id, [parse(draw) for draw in draws.split('; ')]) for game_id, draws in lines]


def part1():
    def is_possible(draws):
        return all(r <= 12 and g <= 13 and b <= 14 for r, g, b in draws)
    return sum(game_id for game_id, draws in lines if is_possible(draws))


def part2():
    rv = 0
    for _, draws in lines:
        max_colors = [0, 0, 0]
        for draw in draws:
            for i in range(3):
                max_colors[i] = max(draw[i], max_colors[i])
        rv += max_colors[0] * max_colors[1] * max_colors[2]
    return rv


print('Part 1:', part1())
print('Part 2:', part2())
