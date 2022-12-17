DATA_FILE = 'data/data.txt'

with open(DATA_FILE) as f:
    raw_data = f.readlines()

best = 0
curr = 0
for s in raw_data:
    s = s[:-1]
    if s:
        curr += int(s)
        best = max(curr, best)
    else:
        curr = 0

print(best)