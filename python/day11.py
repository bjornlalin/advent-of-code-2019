import sys
import numpy as nd
import library.intcode_day9 as comp

def next_direction(direction, left):
    if direction == 'up':
        return 'left' if left else 'right'
    if direction == 'left':
        return 'down' if left else 'up'
    if direction == 'down':
        return 'right' if left else 'left'
    if direction == 'right':
        return 'up' if left else 'down'

def next_position(direction, position):
    if direction == 'up':
        return (position[0], position[1]-1)
    if direction == 'left':
        return (position[0]-1, position[1])
    if direction == 'down':
        return (position[0], position[1]+1)
    if direction == 'right':
        return (position[0]+1, position[1])
    
directions = {
    #direction => direction when turning left, direction when turning right, dx, dy
    'up' : ('left','right',0,-1),
    'left' : ('down','up',-1,0), 
    'down' : ('right','left',0,1), 
    'right' : ('up','down',1,0)
}

def _debug(str):
    if False:
        print(str)

class Robot:

    def __init__(self, program):
        self.intcode = comp.IntComp(list(program), debug=False)
        self.n_outputs_seen = 0
        self.hull = {}
        self.painted = {}
        self.direction = 'up'
        self.pos = (0,0)
        self.minx = 1000
        self.miny = 1000
        self.maxx = 0
        self.maxy = 0
    
    def output(self, output):
        if self.n_outputs_seen % 2 == 0:

            # paint hull white when it was black
            _debug('painting {} as {}'.format(self.pos, output))
            self.hull[self.pos] = output

        else:
            # turn and take a step
            _debug('direction {}, turning to move {}'.format(self.direction, directions[self.direction][output]))
            self.direction = next_direction(self.direction, True if output == 0 else False)
            self.pos = next_position(self.direction, self.pos)

            # Needed for painting the map
            self.minx = self.pos[0] if self.pos[0] < self.minx else self.minx
            self.maxx = self.pos[0] if self.pos[0] > self.maxx else self.maxx
            self.miny = self.pos[1] if self.pos[1] < self.miny else self.miny
            self.maxy = self.pos[1] if self.pos[1] > self.maxy else self.maxy
        
        self.n_outputs_seen += 1

    def run(self, initial=0):
        self.hull[self.pos] = initial
        stopped = False
        while not stopped:
            input = self.hull[self.pos] if self.pos in self.hull else 0
            _debug("sending input: {}".format(input))
            self.intcode.add_input(input)
            status = self.intcode.run(self.output)
            status = self.intcode.run(self.output)
            if status[0] == comp.IntComp.FINISHED:
                stopped = True

        return self.hull
                
    def print(self):
        for y in range(self.miny, self.maxy+1):
            for x in range(self.minx, self.maxx+1):
                if (x, y) in self.hull:
                    print('#' if self.hull[(x,y)] == 1 else '.', end='')
                else:
                    print(' ', end='')
            print('')

def solve(line):
    program = line.replace(' ', '').replace('\n', '').split(',')

    # Part 1
    robot = Robot(program)
    hull = robot.run()
    # robot.print()
    print("Part 1: {}".format(len(hull)))

    # Part 2
    print("Part 2: executing...")
    robot = Robot(program)
    robot.run(initial=1)
    robot.print()

for line in sys.stdin:
    solve(line)
