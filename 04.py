with open('04.txt') as f:
    lines = f.readlines()
    lines = [line.strip() for line in lines]

for i, line in enumerate(lines):
    card_id, numbers = line.split(': ')
    card_id = int(card_id.replace('Card', '').strip())
    winning, own = numbers.split(' | ')
    winning = {int(n) for n in winning.strip().split(' ') if n}
    own = {int(n) for n in own.strip().split(' ') if n}
    lines[i] = (card_id, winning, own)

# rv = 0
# for card_id, winning, own in lines:
#     count = len([card for card in own if card in winning])
#     if count > 0:
#         rv += 2 ** (count - 1)


rv = len(lines)
def process_card(card_pos, starting):
    global rv
    _, winning, own = lines[card_pos]
    count = sum(1 for card in own if card in winning)
    rv += count
    for i in range(count):
        process_card(card_pos + i + 1, starting)

for i, (_, winning, own) in enumerate(lines):
    process_card(i, i)

print(rv)