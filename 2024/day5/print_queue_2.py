from collections import defaultdict

DATA_FILE = 'data/data.txt'

with open(DATA_FILE) as f:
    raw_data = f.readlines()


def is_valid(update: list[str], rules: dict[str, set[str]]) -> bool:
    for i, i1 in enumerate(update):
        for i2 in update[i + 1:]:
            if i1 in rules[i2]:
                return False
    return True


def fix(update: list[str], rules: dict[str, set[str]]) -> list[str]:
    update_set = set(update)
    minirules = rules.copy()
    for key in list(minirules.keys()):
        if key not in update_set:
            del minirules[key]
        else:
            minirules[key] = minirules[key].intersection(update_set)

    l = sorted([(len(after), key, sorted(after)) for key, after in minirules.items()])
    return [key for _, key, _ in l[::-1]]


parsing_rules = True
rules: dict[str, set[str]] = defaultdict(set)
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
        if not is_valid(update, rules):
            result = fix(update, rules)
            middle_idx = len(update) // 2
            total += int(result[middle_idx])

print(total)
