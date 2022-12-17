from falling_sand import draw, parse, simulate

DATA_FILE = 'data/data.txt'


with open(DATA_FILE) as f:
    raw_data = [l.strip() for l in f.readlines()]


obstructions, x_min, x_max, y_min, y_max = parse(raw_data)

count = 0
while simulate(obstructions, y_max):
    count += 1

draw(obstructions, x_min, x_max, y_min, y_max)
print(count)
