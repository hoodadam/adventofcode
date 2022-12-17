DATA_FILE = 'data/sonar_sweep.txt'

with open(DATA_FILE) as f:
    raw_data = f.readlines()
depths = [int(line) for line in raw_data]
print(sum(1 for (a, b, c, d) in zip(depths, depths[1:], depths[2:], depths[3:]) if b + c + d > a + b + c))

