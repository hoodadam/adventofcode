DATA_FILE = 'data/data.txt'

with open(DATA_FILE) as f:
    raw_data = f.readlines()


x_max, y_max = [int(n) for n in raw_data[0].split()]
x_mid, y_mid = x_max // 2, y_max // 2
quadrants = [0, 0, 0, 0]

for robot in raw_data[1:]:
    position, velocity = robot.split()
    p_x, p_y = [int(n) for n in position[2:].split(",")]
    v_x, v_y = [int(n) for n in velocity[2:].split(",")]

    final_x = (p_x + 100 * v_x) % x_max
    final_y = (p_y + 100 * v_y) % y_max

    if final_x < x_mid and final_y < y_mid:
        quadrant = 0
    elif final_x < x_mid and final_y > y_mid:
        quadrant = 1
    elif final_x > x_mid and final_y > y_mid:
        quadrant = 2
    elif final_x > x_mid and final_y < y_mid:
        quadrant = 3
    else:
        continue

    quadrants[quadrant] += 1

print(quadrants[0] * quadrants[1] * quadrants[2] * quadrants[3])