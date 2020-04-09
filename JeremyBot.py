from Player import Player
import random
from itertools import combinations_with_replacement
from collections import defaultdict


class JeremyBot(Player):
    def __init__(self):
        every_possible_combo = []
        for dice_roll in combinations_with_replacement(range(1, 7), 4):
            every_possible_combo.append(JeremyBot.roll_combos(dice_roll))

        self.probs = defaultdict(int)
        for i in range(2, 13):
            for combo_set in every_possible_combo:
                if any([i in pair and pair != (i, i) for pair in combo_set]):
                    self.probs[i] += 1/len(every_possible_combo)

        for combo in combinations_with_replacement(range(2, 13), 2):
            for combo_set in every_possible_combo:
                if combo in combo_set:
                    self.probs[combo] += 1/len(every_possible_combo)
        super().__init__()

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
                                        if col_j != col_i else 0 for col_j in turn_progress))
                E += self.probs[(col_i, col_i)]*((turn_progress[col_i] + 2)/self.probs[col_i]
                                                 + sum(turn_progress[col_j]/self.probs[col_j]
                                                 if col_j != col_i else 0 for col_j in turn_progress))
            for col_i, col_j in combinations_with_replacement(turn_progress, 2):
                E += self.probs[(col_i, col_j)]*((turn_progress[col_i] + 1)/self.probs[col_i]
                                                 + (turn_progress[col_j] + 1)/self.probs[col_j]
                                                 + sum(turn_progress[col_k]/self.probs[col_k]
                                                 if col_k not in (col_i, col_j) else 0 for col_k in turn_progress))
            if E < sum(col_i/self.probs[col_i] for col_i in turn_progress):
                return move, True
            else:
                return move, False
        else:
            return move, False

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


