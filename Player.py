import random


class Player:
    def __init__(self):
        pass

    @staticmethod
    def make_move(combos, player_progress, turn_progress):
        choice = random.choice(combos)
        lock_in = random.choice([True, False])
        return choice, lock_in
