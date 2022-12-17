from typing import Union, Optional

DATA_FILE = 'data/test1.txt'


class SnailFishNumber:
    def __init__(self, *, left=None, right=None, val=None):
        # type: (SnailFishNumber, Optional[SnailFishNumber], Optional[SnailFishNumber], Optional[int]) -> None
        if left:
            self.left = left
            self.right = right
            self.val = None
        else:
            assert val is not None and not right
            self.left = None
            self.right = None
            self.val = val

    def is_leaf(self):
        # type: (SnailFishNumber) -> bool
        return self.val is not None

    def magnitude(self):
        return self.val if self.is_leaf() else 3 * self.left.magnitude() + 2 * self.right.magnitude()

    def reduce(self):
        # type: (SnailFishNumber) -> None
        while True:
            if self.explode():
                continue
            if self.split():
                continue
            break

    def explode(self):
        # type: (SnailFishNumber) -> bool
        left_num = None
        explode = None

        right_num = None
        stack = [(self.right, 1), (self.left, 1)]
        while stack:
            node, depth = stack.pop()
            if not explode:
                if node.is_leaf():
                    left_num = node
                else:
                    if depth == 4:
                        explode = node
                    else:
                        stack.append((node.right, depth + 1))
                        stack.append((node.left, depth + 1))
            else:
                if node.is_leaf():
                    right_num = node
                    break
                else:
                    stack.append((node.right, depth + 1))
                    stack.append((node.left, depth + 1))

        if explode:
            if left_num:
                left_num.val += explode.left.val
            if right_num:
                right_num.val += explode.right.val
            explode.left = None
            explode.right = None
            explode.val = 0
            return True
        else:
            return False

    def split(self):
        # type: (SnailFishNumber) -> bool
        if self.is_leaf():
            if self.val > 9:
                self.left = SnailFishNumber(val=self.val // 2)
                self.right = SnailFishNumber(val=self.val - self.left.val)
                self.val = None
                return True
            else:
                return False
        else:
            return self.left.split() or self.right.split()

    def add(self, other):
        # type: (SnailFishNumber, SnailFishNumber) -> SnailFishNumber
        result = SnailFishNumber(left=self.copy(), right=other.copy())
        result.reduce()
        return result

    @staticmethod
    def parse(number_str):
        # type: (str) -> SnailFishNumber
        cursor = 0

        def _read_char():
            # type: () -> str
            nonlocal cursor
            result = number_str[cursor]
            cursor += 1
            return result

        def _parse_internal():
            # type: () -> Union[SnailFishNumber, int]
            c = _read_char()
            if c == '[':
                left = _parse_internal()
                assert _read_char() == ','
                right = _parse_internal()
                assert _read_char() == ']'
                return SnailFishNumber(left=left, right=right)
            elif c in '0123456789':
                return SnailFishNumber(val=int(c))

        return _parse_internal()

    def __repr__(self):
        if self.is_leaf():
            return str(self.val)
        else:
            return f'[{self.left},{self.right}]'

    def copy(self):
        return SnailFishNumber(val=self.val) if self.is_leaf() \
            else SnailFishNumber(left=self.left.copy(), right=self.right.copy())


if __name__ == '__main__':
    with open(DATA_FILE) as f:
        raw_data = f.read()

    lines = raw_data.splitlines()
    current = None
    for line in lines:
        if current:
            current = current.add(SnailFishNumber.parse(line))
        else:
            current = SnailFishNumber.parse(line)

    print(current)
    print(current.magnitude())
