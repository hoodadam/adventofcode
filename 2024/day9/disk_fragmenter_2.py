DATA_FILE = 'data/data.txt'

with open(DATA_FILE) as f:
    raw_data = f.readlines()

input = raw_data[0].strip()

summary = [int(c) for c in input]
file_sizes = summary[::2]
gaps = summary[1::2]

file_locations = [0]
gap_locations = []
for i in range(1, len(file_sizes)):
    gap_locations.append(file_locations[i-1] + file_sizes[i-1])
    file_locations.append(gap_locations[i-1] + gaps[i-1])

total = 0
for i in range(len(file_sizes) - 1, -1, -1):
    file_size = file_sizes[i]
    for j in range(i):
        gap_size = gaps[j]
        if file_size <= gaps[j]:
            gaps[j] -= file_size
            file_locations[i] = gap_locations[j]
            gap_locations[j] += file_size
            break

print(
    sum(
        id * file_size * (2 * location + file_size - 1) // 2
        for id, (file_size, location) in enumerate(zip(file_sizes, file_locations))
    )
)
