DATA_FILE = 'data/data.txt'

with open(DATA_FILE) as f:
    raw_data = f.readlines()

l1, l2 = [], []
for line in raw_data:
    s1, s2 = line.split()
    l1.append(int(s1))
    l2.append((int(s2)))

l1.sort()
l2.sort()

print(sum(abs(i2 - i1) for i1, i2 in zip(l1, l2)))