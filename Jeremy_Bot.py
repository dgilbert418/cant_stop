from Player import Player
import random

class Jeremy_Bot(Player):

    def __init__(self):
        pass

    def make_move(self, combos, player_progress, turn_progress):
        choice = random.choice(combos)
        lock_in = random.choice([True, False])
        return choice, lock_in
