from collections import defaultdict

DATA_FILE = 'data/data.txt'

with open(DATA_FILE) as f:
    raw_data = f.readlines()


height = len(raw_data)
width = len(raw_data[0].strip())

antennae_by_freq: dict[str, list[tuple[int, int]]] = defaultdict(list)
for i, line in enumerate(raw_data):
    for j, c in enumerate(line.strip()):
        if c != ".":
            antennae_by_freq[c].append((i, j))

antinodes: set[tuple[int, int]] = set()
for freq, antennae in antennae_by_freq.items():
    for i, (a1_i, a1_j) in enumerate(antennae):
        for a2_i, a2_j in antennae[i+1:]:
            antinodes.add((2*a1_i - a2_i, 2*a1_j - a2_j))
            antinodes.add((2*a2_i - a1_i, 2*a2_j - a1_j))

count = sum(1 for i, j in antinodes if (-1 < i < height) and (-1 < j < width))
print(count)
