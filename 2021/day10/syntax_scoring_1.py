DATA_FILE = 'data/actual.txt'

with open(DATA_FILE) as f:
    raw_data = f.read()

mapping = {'(': ')', '[': ']', '{': '}', '<': '>'}
scores = {')': 3, ']': 57, '}': 1197, '>': 25137}
lines = raw_data.splitlines()
score = 0
for line in lines:
    stack = []
    for c in line:
        if c in mapping:
            stack.append(c)
        elif not (stack and c == mapping[stack.pop()]):
            score += scores[c]
            break

print(score)