from Gamestate import Gamestate
#from JeremyBot import JeremyBot
from DodgerBot import DodgerBot
from Player import Player
from GameManager import GameManager
#from itertools import combinations
#from itertools import permutations
#from itertools import chain
#from itertools import product
#import BotLib

bad_players = [DodgerBot(2), DodgerBot(3)]
my_game = GameManager(bad_players)
my_game.execute_game()
#winners = {0: 0, 1: 0}
#for i in range(1000):
#    if i % 1000 == 0:
#        print(i)
#    winner = my_game.execute_game()
#    winners[winner] += 1
#print(winners)

#lane_counts = {}
#for i in range(2, 13):
#    lane_counts[i] = 0
#for d_1 in range(1,7):
#    for d_2 in range(1,7):
#        for d_3 in range(1,7):
#            for d_4 in range(1,7):
#                all_combos = [[d_1 + d_2, d_3 + d_4], [d_1 + d_3, d_2 + d_4], [d_1 + d_4, d_2 + d_3]]
#                for i in range(2, 13):
#                    if i in chain(*all_combos):
#                        lane_counts[i] += 1
#total = 6**4
#lane_probs = [i/total for i in lane_counts.values()]
#print(lane_probs)

