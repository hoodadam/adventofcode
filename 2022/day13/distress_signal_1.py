from list_compare import compare

DATA_FILE = 'data/data.txt'


with open(DATA_FILE) as f:
    raw_data = f.read()


pairs = raw_data.split('\n\n')
tot = 0
for i, pair in enumerate(pairs):
    left, right = [eval(s) for s in pair.split('\n')]
    if compare(left, right) == -1:
        tot += i + 1

print(tot)

