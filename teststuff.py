#from Gamestate import Gamestate
#from Jeremy_Bot import Jeremy_Bot
#from GameManager import GameManager

#bad_players = [Jeremy_Bot(), Jeremy_Bot(), Jeremy_Bot(), Jeremy_Bot()]
#my_game = GameManager(bad_players)

#my_game.execute_game()

import numpy
import pandas as pd


from Gamestate import Gamestate

gamestate = Gamestate.new_board(4, 0)
gamestate.print_state()
gamestate.advance([2, 7])
gamestate.print_state()
gamestate.advance([2, 8])
gamestate.print_state()
gamestate.lock_in()
gamestate.next_player()
gamestate.print_state()
gamestate.advance([4,5])
gamestate.advance([4,5])
gamestate.lock_in()
gamestate.next_player()
gamestate.print_state()