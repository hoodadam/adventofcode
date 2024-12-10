DATA_FILE = 'data/data.txt'

with open(DATA_FILE) as f:
    raw_data = f.readlines()

total = 0
for s in raw_data:
    report = [int(ss) for ss in s.split()]
    sign = 1 if report[-1] > report[0] else -1
    for i1, i2 in zip(report, report[1:]):
        diff = sign * (i2 - i1)
        if diff < 1 or diff > 3:
            break
    else:
        total += 1

print(total)
