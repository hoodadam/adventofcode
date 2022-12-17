DATA_FILE = 'data/actual.txt'


def increment(d, key, val):
    if key not in d:
        d[key] = 0
    d[key] += val


with open(DATA_FILE) as f:
    raw_data = f.read()

template, rules_str = raw_data.split('\n\n')

start = template[0]
end = template[-1]

pairs = {}
for i in range(len(template) - 1):
    s = template[i:i+2]
    increment(pairs, s, 1)

rules = {}
for rule in rules_str.splitlines():
    pair, insert = rule.split(' -> ')
    rules[pair] = insert

for _ in range(40):
    next_step = {}
    for (pair, count) in pairs.items():
        insert = rules[pair]
        increment(next_step, pair[0] + insert, count)
        increment(next_step, insert + pair[1], count)
    pairs = next_step

counts = {start: 1, end: 1}
for (pair, count) in pairs.items():
    increment(counts, pair[0], count)
    increment(counts, pair[1], count)

for element in counts:
    assert counts[element] % 2 == 0
    counts[element] //= 2

print(max(counts.values()) - min(counts.values()))