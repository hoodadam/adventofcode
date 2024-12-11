DATA_FILE = 'data/data.txt'

with open(DATA_FILE) as f:
    raw_data = f.readlines()

input = raw_data[0].strip()

summary = [int(c) for c in input]

disk = [-1] * sum(summary)
id = 0
is_file = True
idx = 0
for size in summary:
    if is_file:
        for i in range(idx, idx+size):
            disk[i] = id
        id += 1
    is_file = not is_file
    idx += size

i = 0
j = len(disk) - 1
while i <= j:
    while disk[i] > -1:
        i += 1

    while disk[j] == -1:
        j -= 1

    if i < j:
        disk[i], disk[j] = disk[j], disk[i]

print(sum(i * n for i, n in enumerate(disk) if n > -1))
