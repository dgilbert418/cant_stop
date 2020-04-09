from Gamestate import Gamestate
from Jeremy_Bot import Jeremy_Bot
from Player import Player
from GameManager import GameManager

bad_players = [Jeremy_Bot(), Player()]
my_game = GameManager(bad_players)
winners = {0: 0, 1: 0}
for i in range(10000):
    if i % 1000 == 0:
        print(i)
    winner = my_game.execute_game()
    winners[winner] += 1
print(winners)

