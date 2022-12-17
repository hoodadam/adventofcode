DATA_FILE = 'data/actual.txt'

with open(DATA_FILE) as f:
    raw_data = f.read()

positions = sorted(int(s) for s in raw_data.split(','))


def compute(pos):
    # type: (int) -> int
    return sum(abs(pos - p) * (abs(pos - p) + 1) // 2 for p in positions)


mean = sum(positions) / len(positions)
guess = round(mean)

curr = compute(guess)
up = compute(guess + 1)

while up < curr:
    guess += 1
    curr = up
    up = compute(guess + 1)

down = compute(guess - 1)
while down < curr:
    guess -= 1
    curr = down
    down = compute(guess - 1)

print(curr)