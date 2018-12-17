from enum import Enum
import subprocess
import time

class CollisionException(Exception):
    def __init__(self, x, y):
        self.x = x
        self.y = y

def clear_screen():
    subprocess.call("cls", shell=True)

class Cart(object):
    def __init__(self, char):
        self.char = char
        self._next_turn = "Left"

    def advance_turn(self):
        turn = self._next_turn

        if self._next_turn == "Left":
            self._next_turn = "Straight"
        elif self._next_turn == "Straight":
            self._next_turn = "Right"
        elif self._next_turn == "Right":
            self._next_turn = "Left"
        else:
            assert("Should not have reached this point")

        return turn

class Map(object):
    def __init__(self, file):
        self._map_layer = []
        self._cart_layer = []

        for line in file:
            map_row = []
            cart_row = []

            for char in line[:-1]:
                if char == ">" or char == "<":
                    map_row.append("-")
                    cart_row.append(Cart(char))
                elif char == "^" or char == "v":
                    map_row.append("|")
                    cart_row.append(Cart(char))
                else:
                    map_row.append(char)
                    cart_row.append(None)

            self._map_layer.append(map_row)
            self._cart_layer.append(cart_row)

    def tick(self):
        cart_positions = []
        for y in range(len(self._cart_layer)):
            for x in range(len(self._cart_layer[y])):
                if self._cart_layer[y][x] is not None:
                    cart_positions.append((x, y))

        for cart_position in cart_positions:
            self._tick_cart(*cart_position)

    def _tick_cart(self, x, y):
        cart = self._cart_layer[y][x]
        self._cart_layer[y][x] = None
        if cart.char == ">":
            x += 1
            if self._cart_layer[y][x] is not None:
                raise CollisionException(x, y)

            if self._map_layer[y][x] == "-":
                cart.char = ">"
            elif self._map_layer[y][x] == "/":
                cart.char = "^"
            elif self._map_layer[y][x] == "\\":
                cart.char = "v"
            elif self._map_layer[y][x] == "+":
                turn = cart.advance_turn()
                if turn == "Left":
                    cart.char = "^"
                elif turn == "Straight":
                    cart.char = ">"
                elif turn == "Right":
                    cart.char = "v"
            else:
                assert("Bad map direction")
        elif cart.char == "<":
            x -= 1
            if self._cart_layer[y][x] is not None:
                raise CollisionException(x, y)

            if self._map_layer[y][x] == "-":
                cart.char = "<"
            elif self._map_layer[y][x] == "/":
                cart.char = "v"
            elif self._map_layer[y][x] == "\\":
                cart.char = "^"
            elif self._map_layer[y][x] == "+":
                turn = cart.advance_turn()
                if turn == "Left":
                    cart.char = "v"
                elif turn == "Straight":
                    cart.char = "<"
                elif turn == "Right":
                    cart.char = "^"
            else:
                assert("Bad map direction")
        elif cart.char == "^":
            y -= 1
            if self._cart_layer[y][x] is not None:
                raise CollisionException(x, y)

            if self._map_layer[y][x] == "|":
                cart.char = "^"
            elif self._map_layer[y][x] == "/":
                cart.char = ">"
            elif self._map_layer[y][x] == "\\":
                cart.char = "<"
            elif self._map_layer[y][x] == "+":
                turn = cart.advance_turn()
                if turn == "Left":
                    cart.char = "<"
                elif turn == "Straight":
                    cart.char = "^"
                elif turn == "Right":
                    cart.char = ">"
            else:
                assert("Bad map direction")
        elif cart.char == "v":
            y += 1
            if self._cart_layer[y][x] is not None:
                raise CollisionException(x, y)

            if self._map_layer[y][x] == "|":
                cart.char = "v"
            elif self._map_layer[y][x] == "/":
                cart.char = "<"
            elif self._map_layer[y][x] == "\\":
                cart.char = ">"
            elif self._map_layer[y][x] == "+":
                turn = cart.advance_turn()
                if turn == "Left":
                    cart.char = ">"
                elif turn == "Straight":
                    cart.char = "v"
                elif turn == "Right":
                    cart.char = "<"
            else:
                assert("Bad map direction")

        self._cart_layer[y][x] = cart


    def print(self):
        for y in range(len(self._map_layer)):
            row = ""
            for x in range(len(self._map_layer[y])):
                if self._cart_layer[y][x]:
                    row += self._cart_layer[y][x].char
                else:
                    row += self._map_layer[y][x]
            print(row)

        
with open("input_file.txt", "r") as file:
    game_map = Map(file)


try:
    while True:
        #clear_screen()
        #game_map.print()
        game_map.tick()
        #time.sleep(1)
except CollisionException as exc:
    print("{},{}".format(exc.x, exc.y))
