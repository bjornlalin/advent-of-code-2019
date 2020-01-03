import sys
import numpy as nd

def _debug(str):
    if False:
        print(str)

def solve(maze):
    # Part 1
    print("Part 1: {}".format('TODO'))
    # Part 2
    print("Part 2: {}".format('TODO'))


# Read maze
maze = {}
row, col = 0, 0
for line in sys.stdin:
    for c in line.strip('\n'):
        maze[(row, col)] = c
        col += 1
    row += 1

solve(maze)