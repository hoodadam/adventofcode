import re

DATA_FILE = 'data/data.txt'

with open(DATA_FILE) as f:
    raw_data = f.readlines()

X_PATTERN = re.compile("X.([0-9]+)")
Y_PATTERN = re.compile("Y.([0-9]+)")
total_cost = 0
for a_str, b_str, prize_str in zip(raw_data[::4], raw_data[1::4], raw_data[2::4]):
    a = int(X_PATTERN.findall(a_str)[0])
    c = int(Y_PATTERN.findall(a_str)[0])
    b = int(X_PATTERN.findall(b_str)[0])
    d = int(Y_PATTERN.findall(b_str)[0])
    X = int(X_PATTERN.findall(prize_str)[0]) + 10000000000000
    Y = int(Y_PATTERN.findall(prize_str)[0]) + 10000000000000

    discriminant = a * d - b * c
    xx = d * X - b * Y
    yy = a * Y - c * X
    if xx % discriminant == 0 and yy % discriminant == 0:
        a_moves = xx // discriminant
        b_moves = yy // discriminant
        total_cost += 3 * a_moves + b_moves

print(total_cost)
