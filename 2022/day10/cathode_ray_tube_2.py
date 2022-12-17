from utils.chunk import chunk

DATA_FILE = 'data/data.txt'


with open(DATA_FILE) as f:
    raw_data = [l.strip() for l in f.readlines()]


x = 1
pixels = []

commands = []
for cmd in raw_data:
    if cmd == 'noop':
        commands.append(0)
    else:
        amount = int(cmd[5:])
        commands.extend([0, amount])

if len(commands) < 240:
    commands.extend([0] * (240 - len(commands)))

for i in range(240):
    pixels.append('#' if abs(x - i % 40) <= 1 else '.')

    amount = commands[i]
    x += amount

rows = chunk(pixels, 40)
for row in rows:
    print(''.join(row))
