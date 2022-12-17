DATA_FILE = 'data/actual.txt'

with open(DATA_FILE) as f:
    raw_data = f.read()

rows = raw_data.splitlines()
grid = [[int(c) for c in row] for row in rows]
m = len(grid)
n = len(grid[0])
total = 0
for i in range(len(grid)):
    for j in range(len(grid[0])):
        val = grid[i][j]
        neighbors = [(i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)]
        if not any(0 <= ii < m and 0 <= jj < n and grid[ii][jj] <= val for (ii, jj) in neighbors):
            total += val + 1

print(total)