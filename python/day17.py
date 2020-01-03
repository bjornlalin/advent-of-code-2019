import sys
import numpy as nd
import library.intcode_day9 as comp

def _debug(str):
    if False:
        print(str)

#
# Get next direction when turning left (param left=True) or right (param left=False)
#
def turn(current, left):
    if current == '^':
        return '<' if left else '>'
    if current == '<':
        return 'v' if left else '^'
    if current == 'v':
        return '>' if left else '<'
    if current == '>':
        return '^' if left else 'v'
    
    print('ERROR')
    return None

def nextpos(pos, direction):
    if direction == '^':
        return (pos[0], pos[1]-1)
    if direction == '<':
        return (pos[0]-1, pos[1])
    if direction == 'v':
        return (pos[0], pos[1]+1)
    if direction == '>':
        return (pos[0]+1, pos[1])

    print('ERROR')
    return None

class Robot:

    def __init__(self, program):
        self.intcode = comp.IntComp(list(program), debug=False)
        self.row = 0
        self.col = 0
        self.grid = nd.zeros(shape=(33,45),dtype=object)
        self.dust = 0

    # Part 1 output function
    def output_grid(self, output):
        if output == 10:
            self.row += 1
            self.col = 0
        else:
            self.grid[self.row, self.col] = chr(output)
            self.col += 1

    # Part 2 output function
    def count_dust(self, output):
        if output > 255:
            self.dust += output

    def intersect(self):
        intersections = set()
        rows = self.grid.shape[0]
        cols = self.grid.shape[1]
        for r in range(0, rows):
            for c in range(0, cols):
                cnt = 0
                if self.grid[r,c] == '#':
                    if r > 0 and self.grid[r-1,c] == '#':
                        cnt += 1
                    if r < (rows-1) and self.grid[r+1,c] == '#':
                        cnt += 1
                    if c > 0 and self.grid[r,c-1] == '#':
                        cnt += 1
                    if c < (cols-1) and self.grid[r,c+1] == '#':
                        cnt += 1
                    
                if cnt == 4:
                    intersections.add((r,c))

        return intersections

    def _horiz_guide(self):
        cols = self.grid.shape[1]
        print('  ', end='')
        for c in range(0, cols):
            print(str(c%10), end='')
        print('')

    def print(self):
        rows = self.grid.shape[0]
        cols = self.grid.shape[1]

        # Print grid + guiding vertical rule
        self._horiz_guide()
        for r in range(0, rows):
            print(str(r%10) + ' ', end='')
            for c in range(0, cols):
                print(self.grid[r, c], end='')
            print('')
        self._horiz_guide()

    def run(self, inputs=[], print_grid=True):

        # Add inputs (needed for part 2)
        for _input in inputs:
            self.intcode.add_input(_input)

        # Run until halted
        stopped = False
        while not stopped:
            if print_grid:
                status = self.intcode.run(self.output_grid)
            else:
                status = self.intcode.run(self.count_dust)
            
            if status[0] == comp.IntComp.FINISHED:
                stopped = True

#def encode_movements(str):
    
def solve(line):
    program = line.replace(' ', '').replace('\n', '').split(',')

    # Part 1

    robot = Robot(program)
    robot.run()
    robot.print()

    sum = 0
    for i in robot.intersect():
        sum += (i[0] * i[1])

    print("Part 1: {}".format(sum))

    # Part 2

    #
    # Solved manually:
    #
    # A R,8,L,12,R,8,
    # B R,12,L,8,R,10,
    # B R,12,L,8,R,10,
    # A R,8,L,12,R,8,
    # C R,8,L,8,L,8,R,8,R,10,
    # A R,8,L,12,R,8,
    # A R,8,L,12,R,8,
    # C R,8,L,8,L,8,R,8,R,10,
    # B R,12,L,8,R,10,
    # C R,8,L,8,L,8,R,8,R,10
    #
    # Input 1:
    # A,B,B,A,C,A,A,C,B,C
    #
    # Input 2 (A)
    # R,8,L,12,R,8
    #
    # Input 3 (B):
    # R,12,L,8,R,10
    #
    # Input 4 (C):
    # R,8,L,8,L,8,R,8,R,10

    inputs = []

    # Movements
    for c in 'A,B,B,A,C,A,A,C,B,C\n':
        inputs.append(ord(c))

    # Movement A
    for c in 'R,8,L,12,R,8\n':
        inputs.append(ord(c))

    # Movement B
    for c in 'R,12,L,8,R,10\n':
        inputs.append(ord(c))

    # Movement C
    for c in 'R,8,L,8,L,8,R,8,R,10\n':
        inputs.append(ord(c))

    # Videofeed y/n
    for c in 'n\n':
        inputs.append(ord(c))

    # Replace instruction at memory 0 with a '2' and execute with the input
    program[0] = '2'
    robot2 = Robot(program)
    robot2.run(inputs=inputs, print_grid=False)

    print("Part 2: {}".format(robot2.dust))

# Fetch input and call solve routine
for line in sys.stdin:
    solve(line)
