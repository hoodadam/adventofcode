from position import Position, CODE_TO_DIRECTION

DATA_FILE = 'data/data.txt'


with open(DATA_FILE) as f:
    raw_data = [l.strip() for l in f.readlines()]


head_pos = Position(0, 0)
followers = [Position(0, 0) for _ in range(9)]


def draw(x_min: int, x_max: int, y_min:int, y_max: int):
    rows = [['.' for _ in range(x_min + x_max + 1)] for _ in range(y_min + y_max + 1)]
    for i, f in enumerate(followers[::-1]):
        rows[y_max - f.y][x_min + f.x] = str(9-i)
    rows[y_max - head_pos.y][x_min + head_pos.x] = 'H'

    for row in rows:
        print(''.join(row))
    print('')


distinct = {(0, 0)}
for move in raw_data:
    parts = move.split(' ')
    direction = CODE_TO_DIRECTION[parts[0]]
    amount = int(parts[1])
    for _ in range(amount):
        head_pos.move(direction)
        prev = head_pos
        for follower in followers:
            follower.follow(prev)
            prev = follower

        tail_pos = followers[-1]
        distinct.add((tail_pos.x, tail_pos.y))

print(len(distinct))


