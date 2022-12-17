DATA_FILE = 'data/dive.txt'

with open(DATA_FILE) as f:
    raw_data = f.readlines()

depth = 0
pos = 0
aim = 0
for line in raw_data:
    [dir, amount_str] = line.split(' ')
    amount = int(amount_str)
    if dir == 'up':
        aim -= amount
    elif dir == 'down':
        aim += amount
    elif dir == 'forward':
        pos += amount
        depth += amount * aim
        if depth < 0:
            raise AssertionError('We can fly!')
    else:
        raise AssertionError(f'Invalid direction: {dir}')

print(depth * pos)
