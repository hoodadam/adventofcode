from monkey import Monkey, parse_monkey


DATA_FILE = 'data/data.txt'


with open(DATA_FILE) as f:
    raw_data = f.read()


n_monkeys = 0
for monkey_str in raw_data.split("\n\n"):
    parse_monkey(monkey_str)
    n_monkeys += 1

for i in range(10000):
    Monkey.do_round(False)

inspections = [Monkey.get(i).inspections for i in range(n_monkeys)]
sorted_inspections = sorted(inspections)
print(sorted_inspections[-2] * sorted_inspections[-1])
