import random
from copy import deepcopy

class GameManager:

    def __init__(self, players):
        num_players = len(players)
        start_player = random.randrange(0, num_players)

        self.gamestate = Gamestate.new_board(num_players, start_player)
        self.players = players

    def query_player(self):
        dice = self.gamestate.dice.copy()
        player_progress = deepcopy(self.gamestate.player_progress)


