import Gamestate
from copy import deepcopy

def i_won(move, player_progress, turn_progress, player_number):
    player_progress_temp = deepcopy(player_progress[player_number])

    for lane in move:
        player_progress_temp[lane] += 1
    for lane in turn_progress:
        player_progress_temp[lane] += 1
    return sum([player_progress_temp[lane] == Gamestate.LANE_LENGTHS[lane] for lane in player_progress_temp]) >= 3
