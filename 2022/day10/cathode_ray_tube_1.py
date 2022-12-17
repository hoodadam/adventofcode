DATA_FILE = 'data/data.txt'


with open(DATA_FILE) as f:
    raw_data = [l.strip() for l in f.readlines()]


tot = 0

x = 1
i = 1
next_num = 20
max_num = 220


def update_tot_if_needed():
    global i, x, next_num, tot
    if i > next_num:
        tot += x * next_num
        next_num += 40


for cmd in raw_data:
    if cmd == 'noop':
        i += 1
        update_tot_if_needed()
    else:
        i += 2
        update_tot_if_needed()
        amount = int(cmd[5:])
        x += amount

print(tot)