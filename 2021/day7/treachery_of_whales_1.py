DATA_FILE = 'data/actual.txt'

with open(DATA_FILE) as f:
    raw_data = f.read()

positions = sorted(int(s) for s in raw_data.split(','))

median = len(positions) // 2
pos = positions[median]
print(sum(abs(p - pos) for p in positions))
