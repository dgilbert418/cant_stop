import random
import numpy
import pandas as pd

class Gamestate:

    NUM_DICE = 4
    NUM_LANES = 11
    LANE_LENGTHS = {2: 3, 3: 5, 4: 7, 5: 9, 6: 11, 7: 13, 8: 11, 9: 9, 10: 7, 11: 5, 12: 3}
    NUM_TEMP_CONES = 3

    def __init__(self, player_progress, turn_progress, cur_player, dice, turn_number):
        self.player_progress = player_progress  # List length NUM_PLAYERS of dicts length NUM_LANES
        self.turn_progress = turn_progress  # Dictionary of up length NUM_TEMP_CONES
        self.cur_player = cur_player
        self.dice = dice
        self.completed_lanes = self.find_completed_lanes()
        self.turn_number = turn_number

    @classmethod
    def new_board(cls, num_players, start_player):
        player_progress = []
        for i in range(num_players):
            p = {}
            for j in cls.LANE_LENGTHS:
                p[j] = 0
            player_progress.append(p)
        turn_progress = {}
        cur_player = start_player
        dice = [0 for i in range(cls.NUM_DICE)]
        turn_number = 0
        board = cls(player_progress, turn_progress, cur_player, dice, turn_number)
        board.roll_dice()
        return board

    def roll_dice(self):
        self.dice = [random.randrange(1, 7) for _ in range(self.NUM_DICE)]

    def advance_lane(self, lane):
        if lane in self.completed_lanes:
            raise CannotAdvanceError(
                "Cannot advance on lane " + str(lane) + "; it is already complete."
            )
        elif lane in self.turn_progress:
            if self.player_progress[self.cur_player][lane] + self.turn_progress[lane] < self.LANE_LENGTHS[lane]:
                self.turn_progress[lane] += 1
            else:
                raise CannotAdvanceError(
                    "Cannot advance on lane " + str(lane) + "; end of lane."
                )
        else:
            if len(self.turn_progress) >= self.NUM_TEMP_CONES:
                raise CannotAdvanceError(
                    "Cannot advance on lane " + str(lane) + "; no more temporary cones."
                )
            else:
                self.turn_progress[lane] = 1

    def advance(self, lanes):
        if not any([self.is_lane_advanceable(i) for i in lanes]):
            raise InvalidCombinationError("Cannot advance on either lane.")
        else:
            for i in lanes:
                if self.is_lane_advanceable(i):
                    self.advance_lane(i)

    def is_lane_advanceable(self, lane):
        if lane in self.completed_lanes:
            return False
        elif lane not in self.turn_progress and len(self.turn_progress) >= 3:
            return False
        elif lane not in self.turn_progress:
            return True
        elif self.player_progress[self.cur_player][lane] + self.turn_progress[lane] >= self.LANE_LENGTHS[lane]:
            return False
        else:
            return True

    def lock_in(self):
        for i in self.turn_progress:
            self.player_progress[self.cur_player][i] += self.turn_progress[i]
        self.completed_lanes = self.find_completed_lanes()

    def next_player(self):
        if self.cur_player == len(self.player_progress) - 1:
            self.cur_player = 0
            self.turn_number += 1
        else:
            self.cur_player += 1
        self.turn_progress = {}

    def find_completed_lanes(self):
        complete = []
        for i in self.LANE_LENGTHS:
            for j in range(len(self.player_progress)):
                if j == self.cur_player and i in self.turn_progress:
                    if self.player_progress[j][i] + self.turn_progress[i] == self.LANE_LENGTHS[i]:
                        complete.append(i)
                else:
                    if self.player_progress[j][i] == self.LANE_LENGTHS[i]:
                        complete.append(i)
        return complete

    def all_combos(self):
        combos = []
        for i in range(1, self.NUM_DICE):
            temp = self.dice.copy()
            lane_1 = temp.pop(i) + temp.pop(0)
            lane_2 = sum(temp)
            valid_lanes = list(filter(self.is_lane_advanceable, [lane_1, lane_2]))
            if valid_lanes:
                combos.append(sorted(valid_lanes))
        return combos

    def winning_player(self):
        for player_id, progress in enumerate(self.player_progress):
            if sum(progress[i] == self.LANE_LENGTHS[i] for i in self.LANE_LENGTHS) >= 3:
                return player_id
        return None

    def print_state(self, colors=('91', '92', '93', '94')):
        textboard = pd.read_csv('textboard.csv', header=None).to_numpy()
        print("Dice: " + str(self.dice))
        print("Current Player: \033[{}mPlayer {}\033[00m".format(colors[self.cur_player],self.cur_player))
        for player_id, progress in enumerate(self.player_progress):
            for lane in progress:
                if progress[lane] > 0:
                    idx = 3*(lane-2)
                    if player_id in [0, 1]:
                        idx += 1
                    else:
                        idx += 2
                    jdx = 3*progress[lane]
                    if player_id in [0,2]:
                        jdx += 0
                    else:
                        jdx += 1
                    textboard[idx, jdx] = "P" + str(player_id)
        for lane in self.turn_progress:
            idx = 3 * (lane - 2)
            if self.cur_player in [0, 1]:
                idx += 1
            else:
                idx += 2
            if lane in self.player_progress[self.cur_player]:
                jdx = 3 * self.turn_progress[lane] + self.player_progress[self.cur_player][lane]
            else:
                jdx = 3 * self.turn_progress[lane]
            if self.cur_player in [0, 2]:
                jdx += 0
            else:
                jdx += 1
            textboard[idx, jdx] = "T"
        n, m = textboard.shape
        for i in range(n):
            for j in range(m):
                if textboard[i, j][0] == 'P':
                    print("\033[{}mX\033[00m".format(colors[int(textboard[i, j][1])]), end="")
                elif textboard[i, j] == 'T':
                    print("\033[{}mT\033[00m".format(colors[self.cur_player]), end="")
                else:
                    print(u"\u001b[38m{}".format(textboard[i, j]), end="")
            print("")
        print("")


class CannotAdvanceError(Exception):
    def __init__(self, message):
        print(message)


class InvalidCombinationError(Exception):
    def __init__(self, message):
        print(message)
