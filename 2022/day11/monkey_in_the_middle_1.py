from monkey import Monkey, parse_monkey


DATA_FILE = 'data/data_test.txt'


with open(DATA_FILE) as f:
    raw_data = f.read()


n_monkeys = 0
for monkey_str in raw_data.split("\n\n"):
    parse_monkey(monkey_str)
    n_monkeys += 1

for _ in range(20):
    Monkey.do_round(True)

inspections = [Monkey.get(i).inspections for i in range(n_monkeys)]
sorted_inspections = sorted(inspections)
print(sorted_inspections[-2] * sorted_inspections[-1])
