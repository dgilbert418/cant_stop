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
        turn_progress = deepcopy(self.gamestate.turn_progress)

        move, lock_in = self.players[self.gamestate.cur_player].make_move(dice, player_progress, turn_progress)

        if self.gamestate.is_legal(move):
            self.gamestate.advance(move)
        else:
            raise IllegalMoveError('Illegal move.')

        if lock_in:
            self.gamestate.lock_in()
        if not self.gamestate.game_over():
            self.query_player()

class IllegalMoveError(Exception):
    def __init__(self, message):
        print(message)
