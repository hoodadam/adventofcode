DATA_FILE = 'data/data.txt'

with open(DATA_FILE) as f:
    lines = f.readlines()


DIRECTIONS = [
    (-1, -1),
    (-1, 0),
    (-1, 1),
    (0, -1),
    (0, 1),
    (1, -1),
    (1, 0),
    (1, 1),
]


count = 0
for i, line in enumerate(lines):
    for j, c in enumerate(line):
        if c == 'X':
            for i_offset, j_offset in DIRECTIONS:
                if (
                        (0 <= i + 3*i_offset < len(lines))
                        and (0 <= j + 3*j_offset < len(line))
                        and lines[i+i_offset][j+j_offset] == 'M'
                        and lines[i+2*i_offset][j+2*j_offset] == 'A'
                        and lines[i+3*i_offset][j+3*j_offset] == 'S'
                ):
                    count += 1

print(count)
