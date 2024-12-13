import re

DATA_FILE = 'data/data.txt'

with open(DATA_FILE) as f:
    raw_data = f.readlines()

X_PATTERN = re.compile("X.([0-9]+)")
Y_PATTERN = re.compile("Y.([0-9]+)")
total_cost = 0
for a_str, b_str, prize_str in zip(raw_data[::4], raw_data[1::4], raw_data[2::4]):
    a_x = int(X_PATTERN.findall(a_str)[0])
    a_y = int(Y_PATTERN.findall(a_str)[0])
    b_x = int(X_PATTERN.findall(b_str)[0])
    b_y = int(Y_PATTERN.findall(b_str)[0])
    prize_x = int(X_PATTERN.findall(prize_str)[0])
    prize_y = int(Y_PATTERN.findall(prize_str)[0])
    min_cost = 0

    for a_moves in range(prize_x // a_x):
        if (
                (prize_x - a_moves * a_x) % b_x == 0
                and (prize_y - a_moves * a_y) % b_y == 0
                and (prize_x - a_moves * a_x) // b_x == (prize_y - a_moves * a_y) // b_y
        ):
            b_moves = (prize_x - a_moves * a_x) // b_x
            cost = a_moves * 3 + b_moves
            if min_cost == 0 or cost < min_cost:
                min_cost = cost

    total_cost += min_cost

print(total_cost)
