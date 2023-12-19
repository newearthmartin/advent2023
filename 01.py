import re

with open('01.txt') as f:
    lines = [line.strip() for line in f.readlines()]


def process(line):
    line = re.sub(r'[A-Za-z]', '', line)
    line = line[0] + line[-1]
    return int(line)


NUMBERS = {
    'one': '1',
    'two': '2',
    'three': '3',
    'four': '4',
    'five': '5',
    'six': '6',
    'seven': '7',
    'eight': '8',
    'nine': '9',
}


def process2(line):
    new_line = ''
    for i, c in enumerate(line):
        if c.isdigit():
            new_line += c
        else:
            for word, num in NUMBERS.items():
                if line.startswith(word, i):
                    new_line += num
                    break
    return int(new_line[0] + new_line[-1])


print('Part 1:', sum(map(process, lines)))
print('Part 2:', sum(map(process2, lines)))