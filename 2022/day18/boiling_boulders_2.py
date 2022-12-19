from typing import Tuple, List


def neighbors(x: int ,y: int, z: int) -> List[Tuple[int, int, int]]:
    return [
        (x + 1, y, z),
        (x - 1, y, z),
        (x, y + 1, z),
        (x, y - 1, z),
        (x, y, z + 1),
        (x, y, z - 1),
    ]


DATA_FILE = 'data/data.txt'

with open(DATA_FILE) as f:
    raw_data = f.readlines()

droplet = {}
for cube in raw_data:
    x, y, z = [int(s) for s in cube.split(',')]
    droplet[(x, y, z)] = 0

x_min = min(x for x, _, _ in droplet) - 1
x_max = max(x for x, _, _ in droplet) + 1
y_min = min(y for _, y, _ in droplet) - 1
y_max = max(y for _, y, _ in droplet) + 1
z_min = min(z for _, _, z in droplet) - 1
z_max = max(z for _, _, z in droplet) + 1

borders = {}
for x, y, z in droplet:
    for c in neighbors(x, y, z):
        if c not in droplet:
            borders[c] = 0
            droplet[(x, y, z)] += 1

for b in borders:
    if borders[b] != 0:
        continue
    curr = set()
    frontier = {b}
    is_bounded = True
    while frontier:
        curr.update(frontier)
        new_frontier = {
            (x, y, z) for c in frontier for x, y, z in neighbors(*c)
            if (
                    (x, y, z) not in curr and
                    (x, y, z) not in droplet and
                    (x_min <= x <= x_max) and
                    (y_min <= y <= y_max) and
                    (z_min <= z <= z_max)
            )
        }
        if any(
            x in {x_min, x_max} or y in {y_min, y_max} or z in {z_min, z_max}
            for x, y, z in new_frontier
        ):
            is_bounded = False
        frontier = new_frontier

    for c in curr:
        if c in borders:
            borders[c] = 1 if is_bounded else 2

for b, val in borders.items():
    if val == 1:
        for c in neighbors(*b):
            if c in droplet:
                droplet[c] -= 1

print(sum(droplet.values()))
