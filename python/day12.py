import sys
import re
import numpy as nd
    
index = 0
pos = nd.zeros((4, 3), dtype=int)
v = nd.zeros((4, 3), dtype=int)

# Read input and create data structures
for line in sys.stdin:
    coords = list(map(lambda x : int(x), re.findall(r"[-]?\d+", line)))
    pos[index] = coords
    index += 1

# Method to move one step
def move(positions, speeds):
    gravity = nd.zeros((4,3), dtype=int)

    # Calculate velocity changes caused by gravity
    for i in range(0, 4):
        for j in range(i+1, 4):
            for col in range(0, 3):
                if positions[i, col] > positions [j, col]:
                    gravity[i, col] -= 1
                    gravity[j, col] += 1
                elif positions[i, col] < positions [j, col]:
                    gravity[i, col] += 1
                    gravity[j, col] -= 1

    speeds += gravity
    positions += speeds

    return positions, speeds

#
# Part 1
############################ 

STEPS = 1000

# Copy original data
positions = nd.copy(pos)
speeds = nd.copy(v)

# Simulate 1000 steps
for i in range(0, STEPS):
    positions, speeds = move(positions, speeds)

# sum up the potential, kinetic and total energy
pot = nd.zeros((4),dtype=int)
kin = nd.zeros((4),dtype=int)
tot = nd.zeros((4),dtype=int)
for row in range(0, 4):
    for col in range(0, 3):
        pot[row] += abs(positions[row, col])
        kin[row] += abs(speeds[row, col])
    tot[row] = pot[row] * kin[row]

# Output result
print("Part 1: Energy after {} steps: {}".format(STEPS, nd.sum(tot)))

#
# Part 2
#
# Key insight is that the axes are independent of each other. Thus we can find a repeating
# cycle for each axis individually, and find the least common multiple of the cycle of all
# three axes.
#
# Note also that the first pattern that should repeat is the initial pattern, since if it is
# deterministic (which it is, it is a linear equation system), that initial pattern will be
# found on the way to any other repeating pattern.
#
############################

import library.utils as util

def repeated(speeds, positions, axis):
    for moon in range(0, 4):
        if not (speeds[moon, axis] == 0 and positions[moon, axis] == pos[moon, axis]):
            return False
    return True


# Find cycles on each axis individually (note this is not very efficient, since we move
# all moons in each step, but it's enough and we can reuse the code from Part 1)
cycles = [-1, -1, -1]
for axis in range(0,3):
    positions = nd.copy(pos)
    speeds = nd.copy(v)
    n = 0
    while True:
        n += 1
        positions, speeds = move(positions, speeds)
        if repeated(speeds, positions, axis):
            cycles[axis] = n
            break

print('Part 2: X repeats after {}, Y repeats after {}, Z repeats after {}. LCM (least common multiple): {}'.format(
    cycles[0], cycles[1], cycles[2], int(util.lcm_3(cycles[0], cycles[1], cycles[2]))))
