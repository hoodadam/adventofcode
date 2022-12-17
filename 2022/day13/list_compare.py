from typing import List, Union


ListOfLists = List[Union[int,'ListOfLists']]


def compare(left: ListOfLists, right: ListOfLists) -> int:
    for l, r in zip(left, right):
        if isinstance(l, int) and isinstance(r, int):
            if l < r:
                return -1
            elif l > r:
                return 1
            else:
                continue

        if isinstance(l, int):
            l = [l]

        if isinstance(r, int):
            r = [r]

        if (cmp := compare(l, r)) != 0:
            return cmp

    if len(left) < len(right):
        return -1
    elif len(left) > len(right):
        return 1
    else:
        return 0
