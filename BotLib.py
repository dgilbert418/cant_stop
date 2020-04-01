import Gamestate

def i_won(self, move, player_progress, turn_progress):
    for lane in move:
        player_progress[lane] += 1
    for lane in turn_progress:
        player_progress[lane] += 1
    return sum([player_progress[lane] == Gamestate.LANE_LENGTHS[lane] for lane in player_progress]) >= 3
