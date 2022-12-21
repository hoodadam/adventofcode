from typing import Dict

DATA_FILE = 'data/data.txt'

with open(DATA_FILE) as f:
    raw_data = f.readlines()


evaluated: Dict[str, int] = {}
not_evaluated: Dict[str, str] = {}
root_checks = ('', '')

for s in raw_data:
    name, eqn = s.split(': ')
    if name == 'root':
        root_checks = eqn[:4], eqn[-5:-1]
        continue

    if name == 'humn':
        continue

    try:
        val = int(eqn)
        evaluated[name] = val
    except Exception as e:
        not_evaluated[name] = eqn


while True:
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

    if not_evaluated == try_again:
        break
    else:
        not_evaluated = try_again

v1, v2 = root_checks
if v2 in evaluated:
    v1, v2 = v2, v1
evaluated[v2] = evaluated[v1]
name = v2
m = evaluated[v2]
while name != 'humn':
    eqn = not_evaluated[name]
    v1, v2, symbol = eqn[:4], eqn[-5:-1], eqn[5]
    if v1 in evaluated:
        n = evaluated[v1]
        if symbol == '+':
            m = m - n
        elif symbol == '-':
            m = n - m
        elif symbol == '*':
            m = m // n
        elif symbol == '/':
            # n / x = c => n // (c + 1) < x <= n // c
            m = n // m
        name = v2
    elif v2 in evaluated:
        n = evaluated[v2]
        if symbol == '+':
            m = m - n
        elif symbol == '-':
            m = m + n
        elif symbol == '*':
            m = m // n
        elif symbol == '/':
            m = m * n
        name = v1
    else:
        raise AssertionError

print(m)
