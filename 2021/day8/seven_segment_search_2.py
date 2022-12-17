DATA_FILE = 'data/actual.txt'

with open(DATA_FILE) as f:
    raw_data = f.read()


class Digit:
    def __init__(self, segments):
        self.segments = segments

    def __hash__(self):
        tot = 0
        for s in self.segments:
            tot *= 2
            tot += s
        return tot

    def __eq__(self, other):
        return isinstance(other, Digit) and self.segments == other.segments

    def __len__(self):
        return sum(self.segments)

    def __sub__(self, other):
        if isinstance(other, Digit):
            return Digit([a and not b for a,b in zip(self.segments, other.segments)])
        else:
            raise TypeError()

    def __repr__(self):
        return ''.join(c for (i, c) in enumerate('abcdefg') if self.segments[i])

    def as_set(self):
        return {c for (i,c) in enumerate('abcdefg') if self.segments[i]}

    @staticmethod
    def parse(digit_str):
        return Digit([c in digit_str for c in 'abcdefg'])


def compute_mapping(input_digits):
    # type: (list[str]) -> dict[Digit, int]
    result = {}
    digits = [Digit.parse(d) for d in input_digits]
    reverse_mapping = [Digit.parse('') for _ in range(10)]
    _069 = []
    _235 = []
    for d in digits:
        if len(d) == 2:
            result[d] = 1
            reverse_mapping[1] = d
        elif len(d) == 3:
            result[d] = 7
            reverse_mapping[7] = d
        elif len(d) == 4:
            result[d] = 4
            reverse_mapping[4] = d
        elif len(d) == 7:
            result[d] = 8
            reverse_mapping[8] = d
        elif len(d) == 6:
            _069.append(d)
        else:
            _235.append(d)

    right = reverse_mapping[1].as_set()
    upper_l = (reverse_mapping[4] - reverse_mapping[1]).as_set()
    lower_l = (reverse_mapping[8] - reverse_mapping[4] - reverse_mapping[7]).as_set()

    for d in _069:
        d_as_set = d.as_set()
        if not right.issubset(d_as_set):
            (bot_r,) = right.intersection(d_as_set)
            result[d] = 6
            reverse_mapping[6] = d
        elif not upper_l.issubset(d_as_set):
            (top_l,) = upper_l.intersection(d_as_set)
            result[d] = 0
            reverse_mapping[0] = d
        elif not lower_l.issubset(d_as_set):
            result[d] = 9
            reverse_mapping[9] = d
        else:
            raise AssertionError()

    for d in _235:
        d_as_set = d.as_set()
        if top_l in d_as_set:
            result[d] = 5
            reverse_mapping[5] = d
        elif bot_r in d_as_set:
            result[d] = 3
            reverse_mapping[3] = d
        else:
            result[d] = 2
            reverse_mapping[2] = d
    return result


total = 0
lines = raw_data.splitlines()
for line in lines:
    inp, output = line.split('|')
    mapping = compute_mapping(inp.split())
    output_digits = output.split()
    num = 0
    for d in output_digits:
        num *= 10
        num += mapping[Digit.parse(d)]
    total += num

print(total)


