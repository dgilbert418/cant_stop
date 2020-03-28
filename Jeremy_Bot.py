from Player import Player

class Jeremy_Bot(Player):

    def __init__(self):
        pass

    def make_move(self, combos, player_progress, turn_progress):
        return combos[0], True