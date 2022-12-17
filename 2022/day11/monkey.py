from typing import List, Callable


class Monkey:
    _monkeys: List['Monkey'] = []
    _max_worry: int = 1

    @classmethod
    def _register(cls, monkey: 'Monkey'):
        cls._monkeys.append(monkey)
        cls._max_worry *= monkey.test

    @classmethod
    def get(cls, idx) -> 'Monkey':
        return cls._monkeys[idx]

    @classmethod
    def do_round(cls, worry_managed: bool):
        for monkey in cls._monkeys:
            monkey.inspect_items(worry_managed)

    def __init__(
            self,
            items: List[int],
            op: Callable[[int], int],
            test: int,
            recipient_if_true: int,
            recipient_if_false: int,
    ) -> None:
        self.items = items
        self.op = op
        self.test = test
        self.recipient_if_true = recipient_if_true
        self.recipient_if_false = recipient_if_false
        self.inspections = 0
        self._register(self)

    def inspect_items(self, worry_managed: bool):
        for item in self.items:
            self.inspections += 1

            new_worry = self.op(item)
            if worry_managed:
                new_worry //= 3
            new_worry = new_worry % self._max_worry
            recipient_idx = self.recipient_if_true if new_worry % self.test == 0 else self.recipient_if_false
            recipient = Monkey.get(recipient_idx)
            recipient.items.append(new_worry)

        self.items = []


def parse_monkey(monkey_str: str) -> None:
    """
    Monkey {i}:
      Starting items: {a0}, {a1}, {a2}, ... {an}
      Operation: new = old *|+ {amount|'old'}
      Test: divisible by {test}
        If true: throw to monkey {j}
        If false: throw to monkey {k}
    """
    lines = monkey_str.split("\n")

    def _parse_items() -> List[int]:
        return [int(i) for i in lines[1][18:].split(', ')]

    def _parse_op() -> Callable[[int], int]:
        sign = lines[2][23]
        amount = lines[2][25:]

        def do_op(old: int) -> int:
            amt = old if amount == 'old' else int(amount)
            if sign == '+':
                return old + amt
            elif sign == '*':
                return old * amt
            else:
                raise AssertionError

        return do_op

    def _parse_int_at(line: int, pos: int) -> int:
        return int(lines[line][pos:])

    items = _parse_items()
    op = _parse_op()
    test = _parse_int_at(3, 21)
    recipient_if_true = _parse_int_at(4, 29)
    recipient_if_false = _parse_int_at(5, 30)
    Monkey(items, op, test, recipient_if_true, recipient_if_false)
