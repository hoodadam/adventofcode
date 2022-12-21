from typing import Dict

DATA_FILE = 'data/data.txt'

with open(DATA_FILE) as f:
    raw_data = f.readlines()


evaluated: Dict[str, int] = {}
not_evaluated: Dict[str, str] = {}

for s in raw_data:
    name, eqn = s.split(': ')
    try:
        val = int(eqn)
        evaluated[name] = val
    except Exception as e:
        not_evaluated[name] = eqn

while 'root' not in evaluated:
    try_again = {}
    for name, eqn in not_evaluated.items():
        v1 = eqn[:4]
        v2 = eqn[-5:-1]
        if v1 in evaluated and v2 in evaluated:
            symbol = eqn[5]
            if symbol == '+':
                evaluated[name] = evaluated[v1] + evaluated[v2]
            elif symbol == '-':
                evaluated[name] = evaluated[v1] - evaluated[v2]
            elif symbol == '*':
                evaluated[name] = evaluated[v1] * evaluated[v2]
            elif symbol == '/':
                evaluated[name] = evaluated[v1] // evaluated[v2]
            else:
                raise AssertionError
        else:
            try_again[name] = eqn

    not_evaluated = try_again

print(evaluated['root'])
