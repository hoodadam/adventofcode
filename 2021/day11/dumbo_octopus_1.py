DATA_FILE = 'data/actual.txt'

with open(DATA_FILE) as f:
    raw_data = f.read()

rows = raw_data.splitlines()
grid = [[int(c) for c in row] for row in rows]
m = len(grid)
n = len(grid[0])


def neighbors(i, j):
    return [(ii, jj) for ii in range(i - 1, i + 2) for jj in range(j-1, j+2) if 0 <= ii < m and 0 <= jj < n and not (i, j) == (ii, jj)]


def iterate():
    flashes = set()
    for i in range(m):
        for j in range(n):
            grid[i][j] += 1
            if grid[i][j] > 9:
                flashes.add((i, j))

    current_flashes = flashes
    while current_flashes:
        next_flashes = set()
        for flash in current_flashes:
            for (i, j) in neighbors(*flash):
                grid[i][j] += 1
                if grid[i][j] > 9 and (i, j) not in flashes:
                    next_flashes.add((i, j))
        flashes = flashes.union(next_flashes)
        current_flashes = next_flashes

    for (i, j) in flashes:
        grid[i][j] = 0

    return len(flashes)


print(sum(iterate() for _ in range(100)))