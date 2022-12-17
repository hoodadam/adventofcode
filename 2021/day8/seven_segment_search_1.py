DATA_FILE = 'data/actual.txt'

with open(DATA_FILE) as f:
    raw_data = f.read()

count = 0
lines = raw_data.splitlines()
for line in lines:
    _, output = line.split('|')
    digits = output.split()
    for digit in digits:
        if len(digit) in {2, 3, 4, 7}:
            count += 1

print(count)
