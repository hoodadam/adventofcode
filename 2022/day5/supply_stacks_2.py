DATA_FILE = 'data/data.txt'


with open(DATA_FILE) as f:
    raw_data = [l.strip() for l in f.readlines()]


n_stacks = int(raw_data[0])
stacks = []
for i in range(1, n_stacks + 1):
    s = raw_data[i]
    stacks.append(list(s.split(',')))


for instruction in raw_data[n_stacks+1:]:
    amount, source, dest = [int(n) for n in instruction.split(',')]

    tmp = []
    for _ in range(amount):
        tmp.append(stacks[source-1].pop())
    for _ in range(amount):
        stacks[dest-1].append(tmp.pop())

print(''.join(s[-1] for s in stacks))