DATA_FILE = 'data/data.txt'

with open(DATA_FILE) as f:
    raw_data = f.readlines()


def is_safe_with_dampener(report: list[int]) -> bool:
    if is_safe(report):
        return True

    for i in range(len(report)):
        if is_safe(report[:i] + report[i+1:]):
            return True

    return False


def is_safe(report: list[int]) -> bool:
    sign = 1 if report[-1] > report[0] else -1
    for i1, i2 in zip(report, report[1:]):
        diff = sign * (i2 - i1)
        if diff < 1 or diff > 3:
            return False
    return True


reports = [[int(ss) for ss in s.split()] for s in raw_data]
print(sum(is_safe_with_dampener(report) for report in reports))
