from Gamestate import Gamestate
from JeremyBot import JeremyBot
from DodgerBot import DodgerBot
from Player import Player
from GameManager import GameManager


bad_players = [DodgerBot(30), DodgerBot(4)]
my_game = GameManager(bad_players)
winners = {0: 0, 1: 0}
for i in range(1000):
    if i % 1000 == 0:
        print(i)
    winner = my_game.execute_game()
    winners[winner] += 1
print(winners)