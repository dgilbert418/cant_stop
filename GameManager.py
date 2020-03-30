import random
from Gamestate import Gamestate
from copy import deepcopy


class GameManager:
    def __init__(self, players):
        num_players = len(players)
        start_player = random.randrange(0, num_players)
        self.gamestate = Gamestate.new_board(num_players, start_player)
        self.players = players

    def query_player(self):
        combos = deepcopy(self.gamestate.all_combos())
        player_progress = deepcopy(self.gamestate.player_progress)
        turn_progress = deepcopy(self.gamestate.turn_progress)

        move, lock_in = self.players[self.gamestate.cur_player].make_move(combos, player_progress, turn_progress)
        return move, lock_in

    def execute_game(self, pause=False):
        while not self.gamestate.winning_player():
            self.gamestate.roll_dice()
            if self.gamestate.is_progress_possible():
                move, lock_in = self.query_player()
            else:
                self.gamestate.next_player()

            if self.gamestate.is_legal(move):
                self.gamestate.advance(move)
            else:
                raise IllegalMoveError('Illegal move.')
            if lock_in:
                self.gamestate.lock_in()
                self.gamestate.next_player()
            self.gamestate.print_state()
            if pause:
                _ = input("Press any key to proceed to the next turn.")
        print("Player " + str(self.gamestate.winning_player()) + "wins the game!")


class IllegalMoveError(Exception):
    def __init__(self, message):
        print(message)