DATA_FILE = 'data/data.txt'

with open(DATA_FILE) as f:
    raw_data = f.readlines()


cubes = set()
for cube in raw_data:
    x, y, z = [int(s) for s in cube.split(',')]
    cubes.add((x, y, z))

tot = 0
for x, y, z in cubes:
    borders = [
        (x + 1, y, z),
        (x - 1, y, z),
        (x, y + 1, z),
        (x, y - 1, z),
        (x, y, z + 1),
        (x, y, z - 1),
    ]
    tot += sum(1 for c in borders if c not in cubes)

print(tot)