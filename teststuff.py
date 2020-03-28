from Gamestate import Gamestate
from Jeremy_Bot import Jeremy_Bot
from GameManager import GameManager

bad_players = [Jeremy_Bot(), Jeremy_Bot(), Jeremy_Bot(), Jeremy_Bot()]
my_game = GameManager(bad_players)

my_game.execute_game()