import re
import time
from collections import deque

class Game(object):
    def __init__(self, players):
        self._scores = deque([0 for i in range(players)])
        self._next_marble_value = 1
        self._game_board = deque()
        self._game_board.append(0)

    def play_round(self):
        if self._next_marble_value % 23 == 0:
            self._resolve_special_marble()
        else:
            self._resolve_normal_marble()

        self._next_marble_value += 1
        self._scores.rotate(-1)
        #self.print_game_state()

    def _resolve_normal_marble(self):
        self._game_board.rotate(-1)
        self._game_board.append(self._next_marble_value)

    def _resolve_special_marble(self):
        self._scores[0] += self._next_marble_value
        self._game_board.rotate(7)
        self._scores[0] += self._game_board.pop()
        self._game_board.rotate(-1)

    def print_game_state(self):
        print(" ".join([str(item) for item in self._game_board]))

    def get_high_score(self):
        return max(self._scores)


def play_game(players, marbles):
    game = Game(players)
    for i in range(marbles + 1):
        game.play_round()
    print("{}/{}: {}".format(players, marbles, game.get_high_score()))

# tests
play_game(9, 25)
play_game(10, 1618)
play_game(13, 7999)
play_game(17, 1104)
play_game(21, 6111)
play_game(30, 5807)

with open("input_file.txt") as file:
    match = re.match(r"(\d+) players; last marble is worth (\d+) points", file.read())
players = int(match.group(1))
marbles = int(match.group(2))
play_game(players, marbles)
start = time.time()
play_game(players, marbles * 100)
print(time.time() - start)
