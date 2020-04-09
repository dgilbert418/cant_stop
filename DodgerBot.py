from Player import Player
import random
import BotLib

class DodgerBot(Player):
# Dodger is known for her steady hand and making random moves

    def __init__(self, eagerness):
        self.eagerness = eagerness
        self.moves_taken = 0

    def make_move(self, combos, player_progress, turn_progress):
        move = random.choice(combos)
        if (self.moves_taken >= self.eagerness) or BotLib.i_won(move, player_progress, turn_progress, self.player_number):
            lock_in = True
            self.moves_taken = 0
        else:
            lock_in = False
            self.moves_taken += 1

        return move, lock_in