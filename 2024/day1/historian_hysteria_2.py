from collections import Counter

DATA_FILE = 'data/data.txt'

with open(DATA_FILE) as f:
    raw_data = f.readlines()

l1, l2 = [], []
for line in raw_data:
    s1, s2 = line.split()
    l1.append(int(s1))
    l2.append((int(s2)))

counter = Counter(l2)
print(sum(counter[i]*i for i in l1))