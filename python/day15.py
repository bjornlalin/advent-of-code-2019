import sys
import numpy as nd
from library.intcode_day9 import IntComp

N = 1
E = 4
S = 2
W = 3
ALLDIRS = [N,W,S,E]

def print_maze(maze):
    rows = [x[0] for x in maze.keys()]
    cols = [x[1] for x in maze.keys()]

    for row in range(min(rows)-1, max(rows)+2):
        for col in range(min(cols)-1, max(cols)+2):
            if (row, col) in maze:
                print('.',end='')
            else:
                print('#',end='')
        print('')

# Human-readable (string) mappings for direction values
def as_c(dir):
    if dir == None:
        return '?'
    return ['','N','S','W','E'][dir]

# reverse direction
def reverse(dir):
    return { N:S, W:E, S:N, E:W }[dir]

# move one step in a direction
def next_pos(pos, dir):
    if dir == N:
        return (pos[0], pos[1] - 1)
    if dir == E:
        return (pos[0]+1, pos[1])
    if dir == S:
        return (pos[0], pos[1] + 1)
    if dir == W:
        return (pos[0]-1, pos[1])

#
# DFS search algorithm using a robot to traverse labyrintg
#
class DFS:
    def __init__(self, robot):
        self.robot = robot
        self.robot_clone_at_oxygen_pos = None
        self.oxygen_pos = None
        self.oxygen_dist = -1
        self.distances = {}
    
    def solve(self):

        for d in ALLDIRS:
            self._search((0,0), d, [])

        print("Part 1: Oxygen tank is {} steps away".format(self.oxygen_dist))

        # After first run, we have a copy of memory for the robot at position of the oxygen tank.
        # We should also reset the maze array with distances from origin to each position at this point.
        self.robot = self.robot_clone_at_oxygen_pos
        self.distances = {}

        # Now we run again, searching from the oxygen tank and recording the distance to each position
        for d in ALLDIRS:
            self._search(self.oxygen_pos, d, [])

        print("Part 2: It takes {} minutes to fill the ship with oxygen".format(max(self.distances.values())))

    def _search(self, from_pos, dir, _path):

        # Move and check if we could move (return code)
        self.robot.move(dir)
        result = self.robot.move_result()

        # We hit a wall and didn't move.
        if result == 0:
            return

        # Update position
        curr_pos = next_pos(from_pos, dir)
        curr_path = _path + [curr_pos]

        # Do not continue if we have already been here on a shorter path than the current one
        if curr_pos in self.distances.keys() and len(curr_path) > self.distances[curr_pos]:
            return

        # Keep track of shortest distance to each position in the maze
        self.distances[curr_pos] = len(curr_path)

        #print('Took a step from position {} in direction {} to position {} (search depth is {})'.format(from_pos, as_c(dir), curr_pos, len(curr_path)))

        # keep track of oxygen tank position and clone robot memory at that point 
        # (to re-do DFS and calculate distance from that point for part 2 in next step)
        if result == 2:
            self.oxygen_pos = curr_pos
            self.oxygen_dist = len(curr_path)
            self.robot_clone_at_oxygen_pos = self.robot.clone()

        # Continue searching if we are on a path
        elif result == 1:
            for d in list(set(ALLDIRS) - set([reverse(dir)])):
                self._search(curr_pos, d, curr_path)

        # After searching in all directions from here, backtrack by taking a step in the direction we came from
        #print('  backtracked to {} (search depth is {})'.format(from_pos, len(_path)))
        self.robot.move(reverse(dir))

#
# Robot wraps an IntCode computer, takes movement instructions and provides output values from the IntCode.
#
class Robot:

    def __init__(self, program):
        self.comp = IntComp(program)
        self._output = -1

    # Clone all internal state
    def clone(self):
        clone = Robot([])
        clone.comp = self.comp.clone()
        return clone

    # Send movement command as input to IntCode
    def move(self, dir):
        self.comp.add_input(dir)
        self.resume()
    
    # Get the last output from IntCode
    def move_result(self):
        return self._output

    # Callback for output from IntCode
    def output(self, value):
        self._output = value

    # Continue executing IntCode (it halts on output)
    def resume(self):
        self.comp.run(self.output)

for line in sys.stdin:
    program = line.replace(' ', '').replace('\n', '').split(',')
    DFS(Robot(program)).solve()
