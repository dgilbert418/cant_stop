import random
from Gamestate import Gamestate
from copy import deepcopy
import random


class GameManager:
    def __init__(self, players):
        for i, player in enumerate(players):
            player.player_number = i
        self.players = players

    def query_player(self):
        combos = deepcopy(self.gamestate.all_combos())
        player_progress = deepcopy(self.gamestate.player_progress)
        turn_progress = deepcopy(self.gamestate.turn_progress)

        move, lock_in = self.players[self.gamestate.cur_player].make_move(combos, player_progress, turn_progress)
        return move, lock_in

    def execute_game(self, pause=False, verbose=False, start_player=None):
        if start_player is None:
            start_player = random.randrange(len(self.players))
        self.gamestate = Gamestate.new_board(len(self.players), start_player)
        while self.gamestate.winning_player() is None:
            if verbose:
                print("All_combos: " + str(self.gamestate.all_combos()))
                print("Winning player: " + str(self.gamestate.winning_player()))
                self.gamestate.print_state()

            self.gamestate.roll_dice()
            if len(self.gamestate.all_combos()) > 0:
                move, lock_in = self.query_player()
                if verbose:
                    print("Player makes move: " + str(move))

                if sorted(move) in self.gamestate.all_combos():
                    self.gamestate.advance(move)
                else:
                    raise IllegalMoveError('Illegal move.')
                if lock_in:
                    self.gamestate.lock_in()
                    self.gamestate.next_player()

                if pause:
                    input("Press any key to proceed to the next turn.")
            else:
                if verbose:
                    print("Player busts!")
                self.gamestate.next_player()

        if verbose:
            print("Player " + str(self.gamestate.winning_player()) + " wins the game!")
        return self.gamestate.winning_player()



class IllegalMoveError(Exception):
    def __init__(self, message):
        print(message)