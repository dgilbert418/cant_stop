from Player import Player
import random
import BotLib
from itertools import product, chain
from collections import defaultdict

class JeremyBot(Player):
    def __init__(self):
        every_combo_set = [JeremyBot.roll_combos(dice_roll) for dice_roll in product(range(1, 7), repeat=4)]
        sum_probs = defaultdict(float)
        for i in range(2, 13):
            for combo_set in every_combo_set:
                if i in chain(*combo_set):
                    sum_probs[i] += 1/len(every_combo_set)
        self.sum_probs = dict(sum_probs)
        self.every_combo_set = every_combo_set
        super().__init__()

    # def calculate_advance_probs(self, turn_progress):
    #     for col in turn_progress:
    #         for combo_set in self.every_combo_set:

    def make_move(self, combos, player_progress, turn_progress):
        combos = [tuple(combo) for combo in combos]
        combo_points = defaultdict(int)
        for combo in combos:
            for col in combo:
                if col in player_progress[self.player_number]:
                    combo_points[combo] += 1
        if combo_points:
            move = max(combo_points, key=combo_points.get)
        else:
            move = random.choice(combos)

        if BotLib.i_won(move, player_progress, turn_progress, self.player_number):
            return move, True

        for col in move:
            if col in turn_progress:
                turn_progress[col] += 1
            else:
                turn_progress[col] = 1

        if len(turn_progress) >= 3:
            E = 0
            for col_i in turn_progress:
                E += self.probs[col_i]*((turn_progress[col_i] + 1)/self.probs[col_i]
                                        + sum(turn_progress[col_j]/self.probs[col_j]
                                        for col_j in filter(lambda x: x != col_i, turn_progress)))
                E += self.probs[(col_i, col_i)]*((turn_progress[col_i] + 2)/self.probs[col_i]
                                                 + sum(turn_progress[col_j]/self.probs[col_j]
                                                 for col_j in filter(lambda x: x != col_i, turn_progress)))
            for col_i in turn_progress:
                for col_j in filter(lambda x: x > col_i, turn_progress):
                    E += self.probs[(col_i, col_j)]*((turn_progress[col_i] + 1)/self.probs[col_i]
                                                     + (turn_progress[col_j] + 1)/self.probs[col_j]
                                                     + sum(turn_progress[col_k]/self.probs[col_k]
                                                     for col_k in filter(lambda x: x not in (col_i, col_j), turn_progress)))
            if E < sum(col_i/self.probs[col_i] for col_i in turn_progress):
                return move, True
        return move, False

    @staticmethod
    def roll_combos(dice):
        combos = set()
        for i in range(len(dice)):
            temp = list(dice)
            lane_1 = temp.pop(i) + temp.pop(0)
            lane_2 = sum(temp)
            valid_lanes = tuple(sorted([lane_1, lane_2]))
            if valid_lanes:
                combos.add(valid_lanes)
        return frozenset(combos)


