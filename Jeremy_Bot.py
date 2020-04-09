from Player import Player
import random
from itertools import combinations_with_replacement
from collections import defaultdict


class Jeremy_Bot(Player):
    def __init__(self):
        every_possible_combo = []
        for dice_roll in combinations_with_replacement(range(1, 7), 4):
            every_possible_combo.append(Jeremy_Bot.roll_combos(dice_roll))

        self.probs = defaultdict(int)
        for i in range(2, 13):
            for combo_set in every_possible_combo:
                if any([i in pair for pair in combo_set]):
                    self.probs[i] += 1/len(every_possible_combo)

        for combo in combinations_with_replacement(range(2, 13), 2):
            for combo_set in every_possible_combo:
                if combo in combo_set:
                    self.probs[combo] += 1/len(every_possible_combo)

    @staticmethod
    def roll_combos(dice):
        combos = []
        for i in range(len(dice)):
            temp = list(dice)
            lane_1 = temp.pop(i) + temp.pop(0)
            lane_2 = sum(temp)
            valid_lanes = tuple(sorted([lane_1, lane_2]))
            combos.append(valid_lanes)
        return set(combos)

    #Choosing random from combos right now.
    def make_move(self, combos, player_progress, turn_progress):
        if len(turn_progress) >= 3:
            expected_progress = 0
            for col in turn_progress:
                expected_progress += 1 + self.probs[col]*sum(turn_progress[col_k]/self.probs[col_k] for col_k in turn_progress)
                expected_progress += self.probs[(col, col)]/self.probs[col]*sum(turn_progress[col_k]/self.probs[col_k] for col_k in turn_progress)
            for col_i, col_j in combinations_with_replacement(turn_progress, 2):
                expected_progress += self.probs[(col_i, col_j)]*(1/self.probs[col_i] + 1/self.probs[col_j])*sum(turn_progress[col_k]/self.probs[col_k] for col_k in turn_progress)

            if expected_progress > sum(col_k/self.probs[col_k] for col_k in turn_progress):
                return random.choice(combos), False
            else:
                return random.choice(combos), True
        else:
            return random.choice(combos), False


