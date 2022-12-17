DATA_FILE = 'data/data.txt'


with open(DATA_FILE) as f:
    raw_data = [l.strip() for l in f.readlines()]


def pri(c):
    b = ord(c)
    if b < 91:
        return b - 38
    else:
        return b - 96


tot = 0
for s in raw_data:
    k = len(s) // 2
    common = set(s[:k]).intersection(set(s[k:]))
    tot += sum(pri(c) for c in common)

print(tot)