from Gamestate import Gamestate

my_state = Gamestate.new_board(3, 0)

for i in range(2):
    my_state.advance_lane(2)
    my_state.advance_lane(5)
    my_state.advance_lane(11)

my_state.lock_in()

print(my_state.turn_progress)
print(my_state.player_progress)
print(my_state.cur_player)

my_state.next_player()
my_state.next_player()

print(my_state.cur_player)