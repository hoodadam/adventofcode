from position import Position, CODE_TO_DIRECTION

DATA_FILE = 'data/data.txt'


with open(DATA_FILE) as f:
    raw_data = [l.strip() for l in f.readlines()]


head_pos = Position(0, 0)
tail_pos = Position(0, 0)

distinct = {(0, 0)}
for move in raw_data:
    parts = move.split(' ')
    direction = CODE_TO_DIRECTION[parts[0]]
    amount = int(parts[1])
    for _ in range(amount):
        head_pos.move(direction)
        tail_pos.follow(head_pos)
        distinct.add((tail_pos.x, tail_pos.y))

print(len(distinct))


