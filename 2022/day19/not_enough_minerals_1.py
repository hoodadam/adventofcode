from minerals import parse_blueprint, optimize_blueprint

DATA_FILE = 'data/data.txt'

with open(DATA_FILE) as f:
    raw_data = f.readlines()


tot = 0
for i, s in enumerate(raw_data):
    blueprint = parse_blueprint(s)
    max_geodes = optimize_blueprint(blueprint, time=24)
    tot += (i + 1) * max_geodes

print(tot)
