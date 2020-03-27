from Gamestate import Gamestate

my_state = Gamestate.new_board(3, 0)
my_state.roll_dice()
print(my_state.dice)
print(my_state.all_combos())