from functools import reduce

with open('01.txt') as f:
    lines = f.readlines()
    lines = map(lambda line: line.strip(), lines)

# def process(line):
#     line = re.sub('[A-Za-z]', '', line)
#     line = line[0] + line[-1]
#     return int(line)

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

def process(line):
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

lines = map(process, lines)
val = reduce(lambda a, b: a + b, lines)
print(val)