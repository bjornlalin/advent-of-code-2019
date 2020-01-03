import sys
import numpy as nd
from library.intcode_day13 import IntComp

TILE_TYPES = ['empty', 'wall', 'block', 'paddle', 'ball']
TILE_SYMBOLS = [' ', '#', '-', '=', 'o']

class Tile:

    def __init__(self, x, y, tile_type):
        self.pos = (x,y)
        self.tile_type = tile_type

    def __str__(self):
        return "drawing {} at {}".format(TILE_TYPES[self.tile_type], self.pos)

#
# Robot wraps an IntCode computer, takes movement instructions and provides output values from the IntCode.
#
class ArcadeGame:
    
    Width = 43
    Height = 22
    Screen = nd.zeros((Height, Width), dtype='object')

    def __init__(self, program):
        
        # The game itself
        self.comp = IntComp(program)
        
        # State of the board and game
        self.tiles = {}
        self.score = 0

        # Temporary variables for parsing output from game
        self.n = 0
        self.tmp_x = -1
        self.tmp_y = -1

        # keep track of direction of the ball
        self.ball_y = None
        self.ball_x = None

    # Callback for output from IntCode
    def output(self, value):
        if self.n % 3 == 0:
            self.tmp_x = value
        elif self.n % 3 == 1:
            self.tmp_y = value
        else:
            if self.tmp_x == -1 and self.tmp_y == 0:
                self.score = value
            else:
                tile = Tile(self.tmp_x, self.tmp_y, value)
                self.tiles[tile.pos] = tile

        self.n += 1

    def joystick_direction(self):
        b = self.ball()
        p = self.pad()

        if b != None and p != None:
            if p.pos[0] < b.pos[0]:
                return 1 # move paddle right
            elif p.pos[0] > b.pos[0]:
                return -1 # move paddle left

        return 0 # neutral position

    def pad(self):
        if len([tile for tile in self.tiles.values() if tile.tile_type == 3]) > 0:
            return [tile for tile in self.tiles.values() if tile.tile_type == 3][0]
        return None

    def ball(self):
        if len([tile for tile in self.tiles.values() if tile.tile_type == 4]) > 0:
            return [tile for tile in self.tiles.values() if tile.tile_type == 4][0]
        return None
        
    def print_screen(self):

        # copy tiles to screen
        for tile in self.tiles.values():
            self.Screen[tile.pos[1], tile.pos[0]] = TILE_SYMBOLS[tile.tile_type]

        # Print it
        for y in range(0, self.Height):
            for x in range(0, self.Width):
                print(self.Screen[y,x], end='')
            print('')

    # Continue executing IntCode (it halts on output)
    def run(self):
        stopped = False
        while not stopped:
            status = self.comp.run(self.output, self.joystick_direction)
            if status[0] == IntComp.FINISHED:
                stopped = True

# Read program
program = sys.stdin.readline().replace(' ', '').replace('\n', '').split(',')

# Run game
game = ArcadeGame(list(program))
game.run()

# Count number of blocks
n_blocks = 0
for tile in game.tiles.values():
    if tile.tile_type == 2:
        n_blocks += 1

print('Part 1: there are {} blocks on screen'.format(n_blocks))

program[0] = '2'
game = ArcadeGame(list(program))
game.run()

print('Part 2: Final score is {}'.format(game.score))