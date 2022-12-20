from minerals import parse_blueprint, optimize_blueprint

DATA_FILE = 'data/data.txt'

with open(DATA_FILE) as f:
    raw_data = f.readlines()

tot = 1
for i, s in enumerate(raw_data):
    if i > 2:
        break

    blueprint = parse_blueprint(s)
    result = optimize_blueprint(blueprint, time=32)
    print(result)
    tot *= result

print(tot)
