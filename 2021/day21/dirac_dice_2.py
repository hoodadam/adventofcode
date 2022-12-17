class State:
    def __init__(self, p1_pos, p2_pos, p1_score, p2_score, player):
        # type: (State, int, int, int, int) -> None
        self.p1_pos = p1_pos
        self.p2_pos = p2_pos
        self.p1_score = p1_score
        self.p2_score = p2_score
        self.player = player

    def winner(self):
        # type: (State) -> int
        return 1 if self.p1_score >= 21 else 2 if self.p2_score >= 21 else 0

    def update(self, offset):
        # type: (State, int) -> State
        if self.player == 1:
            new_pos = (self.p1_pos + offset - 1) % 10 + 1
            return State(new_pos, self.p2_pos, self.p1_score + new_pos, self.p2_score, 3 - self.player)
        elif self.player == 2:
            new_pos = (self.p2_pos + offset - 1) % 10 + 1
            return State(self.p1_pos, new_pos, self.p1_score, self.p2_score + new_pos, 3 - self.player)
        else:
            raise AssertionError()

    def __eq__(self, other):
        return isinstance(other, State) \
               and self.p1_pos == other.p1_pos \
               and self.p2_pos == other.p2_pos \
               and self.p1_score == other.p1_score \
               and self.p2_score == other.p2_score \
               and self.player == other.player

    def __hash__(self):
        return 21 * 21 * 10 * 10 * (self.player - 1) \
               + 21 * 21 * 10 * self.p1_pos \
               + 21 * 21 * self.p2_pos \
               + 21 * self.p1_score \
               + self.p2_score

    def __repr__(self):
        return f'State[{self.p1_pos}, {self.p2_pos}; {self.p1_score}, {self.p2_score}]'


possible_outcomes = {3: 1, 4: 3, 5: 6, 6: 7, 7: 6, 8: 3, 9: 1}


def simulate_game(starting_positions):
    # type: (list[int]) -> int
    p1_pos, p2_pos = starting_positions
    starting_state = State(p1_pos, p2_pos, 0, 0, 1)
    states = {starting_state: 1}

    while any(state.winner() == 0 for state in states):
        for (state, count) in states.copy().items():
            if state.winner() == 0:
                states.pop(state)
                for (outcome, universes) in possible_outcomes.items():
                    new_state = state.update(outcome)
                    if new_state not in states:
                        states[new_state] = 0
                    states[new_state] += count * universes

    wins = [0, 0]
    for state, universes in states.items():
        wins[state.winner() - 1] += universes

    return max(wins)


print(simulate_game([4, 8]))
print(simulate_game([2, 5]))
