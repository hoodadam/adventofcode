DATA_FILE = 'data/actual.txt'


class Board:
    def __init__(self, nums):
        # type: (Board, list[int]) -> None
        self.nums = nums
        self.nums_to_id = {n: i for (i, n) in enumerate(nums)}
        self.hits = [False for _ in range(25)]

    def num_was_called(self, num):
        # type (Board, int) -> int
        if num in self.nums_to_id:
            self.hits[self.nums_to_id[num]] = True
            return self._check_board()
        else:
            return False

    def _check_board(self):
        # type: (Board) -> bool
        return any(self._check_row_and_col(i) for i in range(5))

    def _check_row_and_col(self, i):
        # type: (Board,int) -> bool
        return all(self.hits[5 * i + j] for j in range(5)) or all(self.hits[i + 5 * j] for j in range(5))

    def score(self):
        # type: (Board) -> int
        return sum(self.nums[i] for i in range(25) if not self.hits[i])

    @staticmethod
    def parse(board_raw):
        # type: (str) -> Board
        nums = [int(s) for s in board_raw.split()]
        assert len(nums) == 25
        return Board(nums)

    @staticmethod
    def _parse_row(row_str):
        # type: (str) -> list[int]
        return [int(s) for s in row_str.split()]


with open(DATA_FILE) as f:
    raw_data = f.read()

[numbers, *boards_raw] = raw_data.split('\n\n')
nums = [int(s) for s in numbers.split(',')]
boards = [Board.parse(board_raw) for board_raw in boards_raw]
active = [True for _ in boards]

for n in nums:
    for i, board in enumerate(boards):
        if active[i] and board.num_was_called(n):
            print(board.score() * n)
            active[i] = False
