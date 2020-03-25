import random


class Gamestate:

    NUM_DICE = 4
    NUM_LANES = 11
    LANE_LENGTHS = {2: 3, 3: 5, 4: 7, 5: 9, 6: 11, 7: 13, 8: 11, 9: 9, 10: 7, 11: 5, 12: 3}
    NUM_TEMP_CONES = 3

    def __init__(self, player_progress, turn_progress, cur_player, dice):
        self.player_progress = player_progress  # List length NUM_PLAYERS of dicts length NUM_LANES
        self.turn_progress = turn_progress  # Dictionary of up length NUM_TEMP_CONES
        self.cur_player = cur_player
        self.dice = dice
        self.completed_lanes = self.find_completed_lanes()

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
        board = cls(player_progress, turn_progress, cur_player, dice)
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

    def is_progress_possible(self):
        all_combinations = [self.dice[i] + self.dice[j]
                            for j in range(i+1, len(self.dice))
                            for i in range(len(self.dice) - 1)]
        possible_lanes = list(set(all_combinations))
        return any([self.is_lane_advanceable(i) for i in possible_lanes])

    def advance(self, lanes):
        if not any([self.is_lane_advanceable(i) for i in lanes]):
            raise InvalidCombinationError("Cannot advance on either lane.")
        else:
            for i in lanes:
                if self.is_lane_advanceable(i):
                    self.advance_lanes(i)

    def is_lane_advanceable(self, lane):
        if lane in self.completed_lanes:
            return False
        elif self.player_progress[self.cur_player][lane] + self.turn_progress[lane] >= self.LANE_LENGTHS[lane]:
            return False
        elif lane not in self.turn_progress and len(self.turn_progress) >= 3:
            return False
        else:
            return True

    def lock_in(self):
        for i in self.turn_progress:
            self.player_progress[self.cur_player][i] += self.turn_progress[i]
        self.completed_lanes = self.find_completed_lanes()
        self.turn_progress = {}
        self.roll_dice()
        self.next_player()

    def next_player(self):
        if self.cur_player == len(self.player_progress) - 1:
            self.cur_player = 0
        else:
            self.cur_player += 1

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

    def is_legal(move):
        return (move in self.all_moves(dice)) and any([is_lane_advanceable(lane) for lane in move])


class CannotAdvanceError(Exception):
    def __init__(self, message):
        print(message)


class InvalidCombinationError(Exception):
    def __init__(self, message):
        print(message)
