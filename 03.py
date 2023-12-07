with open('03.txt') as f:
    lines = f.readlines()
    lines = [line.strip() for line in lines]
symbols = []
numbers = []
for i, line in enumerate(lines):
    number = ''
    number_pos = None
    for j, c in enumerate(line):
        if c.isdigit():
            number += c
            if number_pos is None:
                number_pos = (i,j)
        else:
            if number:
                numbers.append((*number_pos, number))
                number_pos = None
                number = ''
            if c != '.':
                symbols.append((i, j, c))
    if number: 
        numbers.append((*number_pos, number))

# rv = 0
# for ni, nj, num in numbers:
#     for si, sj, _ in symbols:
#         if abs(ni - si) <= 1 and nj - 1 <= sj and sj <= nj + len(num):
#             rv += int(num)
#             break
# print(rv)

rv = 0
for si, sj, sym in symbols:
    if sym != '*': continue
    nums = [int(num) 
                for ni, nj, num in numbers 
                if abs(ni - si) <= 1 and nj - 1 <= sj and sj <= nj + len(num)]
    if len(nums) == 2:
        rv += nums[0] * nums[1]
print(rv)
