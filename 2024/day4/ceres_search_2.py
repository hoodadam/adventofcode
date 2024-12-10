DATA_FILE = 'data/data.txt'

with open(DATA_FILE) as f:
    lines = f.readlines()

count = 0
for i, line in enumerate(lines[1:-1]):
    for j, c in enumerate(line[1:-1]):
        if c == 'A':
            # i and j are both offset by 1
            if (
                    (lines[i][j] == 'M' and lines[i+2][j+2] == 'S' or lines[i][j] == 'S' and lines[i+2][j+2] == 'M')
                    and (lines[i+2][j] == 'M' and lines[i][j+2] == 'S' or lines[i+2][j] == 'S' and lines[i][j+2] == 'M')
            ):
                count += 1

print(count)
