import random


class Player:
    def __init__(self):
        self.player_number = None

    def make_move(self, combos, player_progress, turn_progress):
        choice = random.choice(combos)
        lock_in = random.choice([True, False])
        return choice, lock_in

    @property
    def player_number(self):
        return self.__player_number

    @player_number.setter
    def player_number(self, value):
        self.__player_number = value
