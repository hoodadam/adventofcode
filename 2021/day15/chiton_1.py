import heapq

DATA_FILE = 'data/actual.txt'

with open(DATA_FILE) as f:
    raw_data = f.read()

grid = [[int(c) for c in row] for row in raw_data.splitlines()]
m = len(grid)
n = len(grid[0])
start = (0, 0)
end = (m - 1, n - 1)


def neighbors(i, j):
    possible_neighbors = [(i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)]
    return [(ii, jj) for ii, jj in possible_neighbors if 0 <= ii < m and 0 <= jj < n]


queue = [(0, [start])]
visited = {start}
heapq.heapify(queue)
while queue:
    risk, path = heapq.heappop(queue)
    current_node = path[-1]
    if current_node == end:
        print(risk)
        break

    for (i, j) in neighbors(*current_node):
        if not (i, j) in visited:
            visited.add((i, j))
            heapq.heappush(queue, (risk + grid[i][j], path + [(i, j)]))
