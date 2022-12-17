from bisect import bisect_left
from functools import cmp_to_key

from list_compare import compare

DATA_FILE = 'data/data.txt'


with open(DATA_FILE) as f:
    raw_data = [l.strip() for l in f.readlines()]


inputs = [eval(s) for s in raw_data if s]
key_fn = cmp_to_key(compare)
inputs.sort(key=key_fn)

low_index = bisect_left(inputs, key_fn([[2]]), key=key_fn) + 1
high_index = bisect_left(inputs, key_fn([[6]]), key=key_fn) + 2
print(low_index * high_index)