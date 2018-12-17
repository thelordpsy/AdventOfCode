from enum import Enum
import subprocess
import time

class CompleteException(Exception):
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

            for char in line.rstrip("\n"):
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
        for cart_position in self._get_cart_positions():
            self._tick_cart(*cart_position)

        new_cart_positions = self._get_cart_positions()
        if len(new_cart_positions) == 1:
            raise CompleteException(*new_cart_positions[0])
        #print(new_cart_positions)

    def _get_cart_positions(self):
        cart_positions = []
        for y in range(len(self._cart_layer)):
            for x in range(len(self._cart_layer[y])):
                if self._cart_layer[y][x] is not None:
                    cart_positions.append((x, y))
        return cart_positions

    def _tick_cart(self, x, y):
        cart = self._cart_layer[y][x]
        if cart is None:
            return

        self._cart_layer[y][x] = None
        if cart.char == ">":
            x += 1
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


        if self._cart_layer[y][x] is None:
            self._cart_layer[y][x] = cart
        else:
            # Don't put back this cart, and delete the existing cart
            self._cart_layer[y][x] = None
        


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
except CompleteException as exc:
    #clear_screen()
    #game_map.print()
    print("{},{}".format(exc.x, exc.y))
