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
    for i, (i1, j1) in enumerate(antennae):
        for i2, j2 in antennae[i+1:]:
            di, dj = i2 - i1, j2 - j1
            ii, jj = i1, j1
            while (-1 < ii < height) and (-1 < jj < width):
                antinodes.add((ii, jj))
                ii, jj = ii - di, jj - dj
            ii, jj = i2, j2
            while (-1 < ii < height) and (-1 < jj < width):
                antinodes.add((ii, jj))
                ii, jj = ii + di, jj + dj

count = sum(1 for i, j in antinodes if (-1 < i < height) and (-1 < j < width))
print(count)


