import heapq


DATA_FILE = 'data/data.txt'

with open(DATA_FILE) as f:
    raw_data = f.readlines()

best = []
curr = 0
for s in raw_data:
    s = s[:-1]
    if s:
        curr += int(s)
    else:
        if len(best) < 3:
            heapq.heappush(best, curr)
        else:
            heapq.heappushpop(best, curr)
        curr = 0

heapq.heappushpop(best, curr)

print(sum(best))