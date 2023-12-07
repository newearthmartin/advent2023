from collections import defaultdict
from functools import cmp_to_key
from enum import Enum

class HandType(Enum):
    FIVE = 6
    FOUR = 5
    FULL_HOUSE = 4
    THREE = 3
    TWO_PAIRS = 2
    PAIR = 1
    HIGH_CARD = 0

with open('07.txt') as f:
    hands = f.readlines()
    hands = [hand.strip().split(' ') for hand in hands]
    hands = [[card, int(bid)] for card, bid in hands]

CARD_ORDER1 = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']
CARD_ORDER2 = ['A', 'K', 'Q', 'T', '9', '8', '7', '6', '5', '4', '3', '2', 'J']

def count(cards, include_j=True):
    counter = defaultdict(int)
    counts = defaultdict(int)
    for c in cards: counter[c] += 1
    for c, val in counter.items(): 
        if include_j or c != 'J':
            counts[val] += 1
    return counter, counts

def get_type1(cards):
    _, counts = count(cards)
    if counts[5]: return HandType.FIVE
    if counts[4]: return HandType.FOUR
    if counts[3]: return HandType.FULL_HOUSE if counts[2] else HandType.THREE
    if counts[2] == 2: return HandType.TWO_PAIRS
    if counts[2] == 1: return HandType.PAIR
    return HandType.HIGH_CARD

def get_type2(cards):
    counter, counts = count(cards, include_j=False)
    js = counter['J']
    
    if counts[5]: return HandType.FIVE
    if counts[4]: return HandType.FIVE if js else HandType.FOUR
    if counts[3]:
        if js == 2: return HandType.FIVE
        if js == 1: return HandType.FULL_HOUSE
        if counts[2]: return HandType.FULL_HOUSE
        return HandType.THREE
    if counts[2] >= 2: 
        if js == 1: return HandType.FULL_HOUSE
        return HandType.TWO_PAIRS
    if counts[2] == 1: 
        if js == 3: return HandType.FIVE
        if js == 2: return HandType.FOUR
        if js == 1: HandType.THREE
        return HandType.PAIR
    if js >= 4: return HandType.FIVE
    if js == 3: return HandType.FULL_HOUSE
    if js == 2: return HandType.THREE
    if js == 1: return HandType.PAIR
    return HandType.HIGH_CARD

def process(card_order, type_fn):
    global hands
    for hand in hands: 
        hand.append(type_fn(hand[0]))
    def key_fn(hand):
        return (hand[2].value, [-card_order.index(c) for c in hand[0]])
    hands.sort(key=key_fn)

# process(CARD_ORDER1, get_type1)
process(CARD_ORDER2, get_type2)

rv = 0
for i, (cards, bid, type) in enumerate(hands):
    rv += (i + 1) * bid
    print(cards, type.name, bid, i + 1, (i + 1) * bid)
print(rv)