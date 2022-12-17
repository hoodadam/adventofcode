DATA_FILE = 'data/actual.txt'

with open(DATA_FILE) as f:
    raw_data = f.read()

counts = [0 for _ in range(9)]
for f in raw_data.split(','):
    counts[int(f)] += 1

for _ in range(256):
    counts = [
        counts[1],  # 1 -> 0
        counts[2],  # 2 -> 1
        counts[3],  # 3 -> 2
        counts[4],  # 4 -> 3
        counts[5],  # 5 -> 4
        counts[6],  # 6 -> 5
        counts[7] + counts[0],  # 7, 0 -> 6
        counts[8],  # 8 -> 7
        counts[0],  # 0 -> 8
    ]

print(sum(counts))