DATA_FILE = 'data/actual.txt'

with open(DATA_FILE) as f:
    raw_data = f.read()

rows = raw_data.splitlines()
grid = [[int(c) for c in row] for row in rows]
m = len(grid)
n = len(grid[0])


def get_neighbors(i, j):
    neighbors = [(i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)]
    return [(ii, jj) for (ii, jj) in neighbors if 0 <= ii < m and 0 <= jj < n]


def is_low_point(i, j):
    return all(grid[ii][jj] > grid[i][j] for (ii, jj) in get_neighbors(i, j))


def get_basin_size(i, j):
    basin = {(i, j)}
    boundary = {(i, j)}

    while boundary:
        neighbors = {
            (i2, j2) for (i1, j1) in boundary for (i2, j2) in get_neighbors(i1, j1) if
            (i2, j2) not in basin and grid[i1][j1] < grid[i2][j2] < 9
        }
        boundary = {
            (i1, j1) for (i1, j1) in neighbors if not any((i2, j2) not in basin and grid[i2][j2] < grid[i1][j1] for (i2, j2) in get_neighbors(i1, j1))
        }
        basin = basin.union(boundary)
    return len(basin)


low_points = [(i, j) for i in range(m) for j in range(n) if is_low_point(i, j)]

top3 = [0, 0, 0]

for low_point in low_points:
    size = get_basin_size(*low_point)
    if size > top3[2]:
        top3[2] = size
    if size > top3[1]:
        top3[2], top3[1] = top3[1], top3[2]
    if size > top3[0]:
        top3[0], top3[1] = top3[1], top3[0]

print(top3[0] * top3[1] * top3[2])