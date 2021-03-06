import Gamestate
from copy import deepcopy
from itertools import product, chain, combinations
from collections import defaultdict

def i_won(move, player_progress, turn_progress, player_number):
    player_progress_temp = deepcopy(player_progress[player_number])
    for lane in move:
        player_progress_temp[lane] += 1
    for lane in turn_progress:
        player_progress_temp[lane] += 1
    return sum([player_progress_temp[lane] == Gamestate.LANE_LENGTHS[lane] for lane in player_progress_temp]) >= 3


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

# initialize lane_probs
# key: lane #
# value: probability you can advance at least once on that lane
every_combo_set = [roll_combos(dice_roll) for dice_roll in product(range(1, 7), repeat=4)]
lane_probs = defaultdict(float)
for i in range(2, 13):
    for combo_set in every_combo_set:
        if i in chain(*combo_set):
            lane_probs[i] += 1 / len(every_combo_set)
lane_probs = dict(lane_probs)

# initialize bust_dict
# key: tuple of advanceable lanes
# value: probability you will bust 
bust_dict = {}
lanes = [i for i in range(2,13)]
for j in range(1, 13):
    combos = combinations(lanes, j)
    for c in combos:
        bust_dict[c] = 0

every_combo_set = [roll_combos(dice_roll) for dice_roll in product(range(1, 7), repeat=4)]
for c in every_combo_set:
    for b in bust_dict:
        if len(set(chain(*c)).intersection(set(b))) == 0:
            bust_dict[b] += 1
total = 6**4
for b in bust_dict:
    bust_dict[b] /= total