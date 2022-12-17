DATA_FILE = 'data/actual.txt'

with open(DATA_FILE) as f:
    raw_data = f.read().splitlines()

n = len(raw_data)
m = len(raw_data[0])

totals = [0 for _ in range(m)]
for s in raw_data:
    for (i, c) in enumerate(s):
        totals[i] += int(c)

gamma = 0
eps = 0
for i in range(m):
    gamma *= 2
    eps *= 2
    if totals[i] > n / 2:
        gamma += 1
    elif totals[i] < n / 2:
        eps += 1
    else:
        raise AssertionError('Not sure what to do with this')

print(gamma * eps)