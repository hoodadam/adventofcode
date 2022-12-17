DATA_FILE = 'data/actual.txt'

with open(DATA_FILE) as f:
    raw_data = f.read()

char_mapping = {'(': ')', '[': ']', '{': '}', '<': '>'}
scores_mapping = {')': 1, ']': 2, '}': 3, '>': 4}
lines = raw_data.splitlines()
scores = []
for line in lines:
    stack = []
    for c in line:
        if c in char_mapping:
            stack.append(c)
        elif not (stack and c == char_mapping[stack.pop()]):
            break
    else:
        score = 0
        while stack:
            score *= 5
            score += scores_mapping[char_mapping[stack.pop()]]
        if score:
            scores.append(score)

sorted_scores = sorted(scores)
print(sorted_scores[len(sorted_scores) // 2])