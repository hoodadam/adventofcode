from cave import Cave

DATA_FILE = 'data/data.txt'

with open(DATA_FILE) as f:
    raw_data = f.read()

cave = Cave(raw_data)
for _ in range(2022):
    cave.simulate_rock()

print(cave.height)
