def simulate_game(starting_positions):
    # type: (list[int]) -> int
    positions = starting_positions.copy()
    player = 0
    scores = [0, 0]
    rolls = 0

    def roll():
        # type: () -> int
        nonlocal rolls
        rolls += 1
        return rolls % 100

    while True:
        total = sum(roll() for _ in range(3))
        position = (positions[player] + total - 1) % 10 + 1
        positions[player] = position
        scores[player] += position
        if scores[player] >= 1000:
            return scores[1 - player] * rolls

        player = 1 - player


print(simulate_game([4, 8]))
print(simulate_game([2, 5]))
