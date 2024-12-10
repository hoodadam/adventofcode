from collections import defaultdict

DATA_FILE = 'data/data.txt'

with open(DATA_FILE) as f:
    raw_data = f.readlines()

parsing_rules = True
rules = defaultdict(set)
updates = []
total = 0
for line in raw_data:
    if not line.strip():
        parsing_rules = False
        print()
    elif parsing_rules:
        i1, i2 = line.strip().split("|")
        rules[i1].add(i2)
    else:
        update = line.strip().split(",")
        for i, i1 in enumerate(update):
            for i2 in update[i+1:]:
                if i1 in rules[i2]:
                    break
            else:
                continue
            break
        else:
            middle_idx = len(update) // 2
            total += int(update[middle_idx])

print(total)
