import re
with (open('04.txt') as f):
    lines = (line.strip() for line in f.readlines())
    lines = (line.split(': ')[1] for line in lines)
    lines = (cards.split(' | ') for cards in lines)

    def get_numbers(l):
        return set(map(int, re.findall(r'\d+', l)))
    lines = [(get_numbers(winning), get_numbers(own)) for winning, own in lines]


def part1():
    rv = 0
    for winning, own in lines:
        count = sum(1 for card in own if card in winning)
        if count > 0:
            rv += 2 ** (count - 1)
    return rv


def part2():
    rv = 0

    def process_card(card_pos, starting):
        nonlocal rv
        winning, own = lines[card_pos]
        count = sum(1 for card in own if card in winning)
        rv += count
        for j in range(count):
            process_card(card_pos + j + 1, starting)
    for i in range(len(lines)):
        process_card(i, i)
    return len(lines) + rv


print('Part 1:', part1())
print('Part 2:', part2())