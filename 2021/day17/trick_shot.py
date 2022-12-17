DATA_FILE = 'data/actual.txt'

with open(DATA_FILE) as f:
    raw_data = f.read()

x_range_str, y_range_str = raw_data.split(', ')
x_min, x_max = [int(s) for s in x_range_str.split('..')]
y_min, y_max = [int(s) for s in y_range_str.split('..')]

velocities = []
for v_x in range(1, x_max + 1):
    if v_x * (v_x + 1) // 2 < x_min:
        continue

    for v_y in range(y_min, abs(y_min)):
        x = 0
        y = 0
        t = 0
        while y >= y_min:
            x += max(0, v_x - t)
            y += v_y - t
            t += 1
            if x_min <= x <= x_max and y_min <= y <= y_max:
                velocities.append((v_x, v_y))
                break

best = 0
for _, v_y in velocities:
    if v_y > best:
        best = v_y

print(best * (best + 1) // 2)
print(len(velocities))