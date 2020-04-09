import random


class Player:
    def __init__(self, player_number):
        self.player_number = player_number

    def make_move(self, combos, player_progress, turn_progress):
        choice = random.choice(combos)
        lock_in = random.choice([True, False])
        return choice, lock_in
