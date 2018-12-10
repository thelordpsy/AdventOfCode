import re
import time

# This took an extremely long time to run (1 hour and 3 minutes)
# I'm sure it's purely a data structure issue, and we could resolve it by switching from an array to a custom built structure
# Replacing with collections.deque actually made it take even longer.

class Game(object):
    def __init__(self, players):
        self._players = [0 for i in range(players)]
        self._current_player = 0
        self._current_marble_index = 0
        self._next_marble_value = 1
        self._game_board = [0]

    def play_round(self):
        if self._next_marble_value % 23 == 0:
            self._resolve_special_marble()
        else:
            self._resolve_normal_marble()

        self._next_marble_value += 1
        self._current_player = (self._current_player + 1) % len(self._players)

    def _resolve_normal_marble(self):
        # The marble is inserted 2 slots to the right of the current marble
        if len(self._game_board) == 1:
            insert_index = 1
        else:
            insert_index = (self._current_marble_index + 2) % len(self._game_board)
        self._game_board.insert(insert_index, self._next_marble_value)
        self._current_marble_index = (insert_index) % len(self._game_board)

    def _resolve_special_marble(self):
        self._players[self._current_player] += self._next_marble_value
        second_marble_index = (self._current_marble_index - 7) % len(self._game_board)
        self._players[self._current_player] += self._game_board[second_marble_index]
        del self._game_board[second_marble_index]
        self._current_marble_index = second_marble_index % len(self._game_board)

    def print_game_state(self):
        print(" ".join([self._stringify(item) for item in self._game_board]))

    def print_high_score(self):
        player_score = max(self._players)
        player_id = self._players.index(player_score) + 1
        print("{}: {}".format(player_id, player_score))

    def _stringify(self, item):
        if self._game_board[self._current_marble_index] == item:
            return "({})".format(item)
        return str(item)

with open("input_file.txt") as file:
    match = re.match(r"(\d+) players; last marble is worth (\d+) points", file.read())
players = int(match.group(1))
marbles = int(match.group(2))

game = Game(players)
start = time.time()
for i in range((marbles * 100) + 1):
    game.play_round()
    if i % marbles == 0:
        print("{} / {} | {}% | {}s".format(i, marbles * 100, (i / marbles), time.time() - start))

game.print_high_score()

