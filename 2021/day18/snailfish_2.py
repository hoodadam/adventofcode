from snailfish_1 import SnailFishNumber

DATA_FILE = 'data/actual.txt'

with open(DATA_FILE) as f:
    raw_data = f.read()
numbers = [SnailFishNumber.parse(line) for line in raw_data.splitlines()]

best = 0
best_ns = (None, None)
for i1, n1 in enumerate(numbers):
    for i2, n2 in enumerate(numbers):
        if i1 != i2:
            result = n1.add(n2)
            magnitude = result.magnitude()
            if magnitude > best:
                best = magnitude
                best_ns = (n1, n2)

print(best)
