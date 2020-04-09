from Gamestate import Gamestate
from Jeremy_Bot import Jeremy_Bot
from Player import Player
from GameManager import GameManager

bad_players = [Jeremy_Bot(), Player()]
my_game = GameManager(bad_players)
winners = {0: 0, 1: 0}
for i in range(10000):
    winner = my_game.execute_game()
    winners[winner] += 1
print(winners)


# gamestate = Gamestate.new_board(4, 0)
# gamestate.print_state()
# gamestate.advance([2, 7])
# gamestate.print_state()
# gamestate.advance([2, 8])
# gamestate.print_state()
# gamestate.lock_in()
# gamestate.next_player()
# gamestate.print_state()
# gamestate.advance([4,5])
# gamestate.advance([4,5])
# gamestate.lock_in()
# gamestate.next_player()
# gamestate.print_state()