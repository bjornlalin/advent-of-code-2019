import sys
import numpy as nd
import math
import collections

dim = 30
grid = nd.zeros((dim, dim),dtype=int)

# Count how many asteroids are visible from a particular asteroid at coordinate (row, col)
def visible(grid, row, col):
    seen = set()
    for r in range(0, dim):
        for c in range(0, dim):

            # No star at that coordinate
            if grid[r,c] == 0:
                continue

            # We don't need to consider ourselves
            if c == col and r == row:
                continue

            # Get the angle to each asteroid and add it to the set of ssen asteroids
            angle = math.atan2(r-row,c-col)
            seen.add(angle)
    
    # print("from {} we can see {} stars".format((row, col), len(seen)))
    
    return len(seen)

# Parse input
row = 0
for line in sys.stdin:
    for col in range(0, len(line.strip())):
        if line[col] == '#':
            grid[row, col] = 1
    row += 1

#
# Part 1: find the asteroid from which the largest number of other asteroids are visible
#         we calculate the slope of a line from asteroid X to all other asteroids, and 
#         count the number of unique slope values in each quadrant
#
max_pos = (-1, -1)
max_visible = 0
for row in range(0, dim):
    for col in range(0, dim):
        if grid[row, col] == 1:
            n_visible = visible(grid, row, col)
            if n_visible > max_visible:
                max_visible = n_visible
                max_pos = (row, col)

print("Part 1: from the star at position {} you can see the most other starts, {} of them.".format(max_pos, max_visible))

# We mount the laser on the best asteroid from part 1 
laser_pos = max_pos
space = nd.copy(grid)
asteroids_sorted = collections.defaultdict(list)

#
# Calculate the angle and distance to each asteroid and store
# them sorted on this order.
#
#              (0,22)
#              -PI/2
#                |
#                |
# (25,0)  PI ---(+)--- 0.0   (+) => (25,22)
#                |
#                |
#               PI/2
#             (28,22)
#
for r in range(0, dim):
    for c in range(0, dim):
        if grid[r,c] == 1 and (r,c) != laser_pos:
            dr = r - laser_pos[0]
            dc = c - laser_pos[1]

            # Get angle
            angle = math.atan2(dr,dc)
            angle += math.pi/2
            if angle < 0:
                angle += 2*math.pi

            # Get distance
            dist = math.sqrt(dr*dr + dc*dc)
            
            # Add to data structure
            asteroids_sorted[angle].append((dist, r, c))

#
# With the transformation done, we can sort in ascending order from N and clockwise.
# The idea is to map all asteroids by their angle, and then sort all asteroids with
# the same angle by distance to the laser.
#
# Once this sorting is done, we can iterate the map and shoot down one asteroid after 
# the other until we shoot down the 200th asteroid. This should be the answer to part 2.
#
shotdown = 0
while True:
    for key in sorted(asteroids_sorted.keys()):
        if len(asteroids_sorted[key]) > 0:
            destroyed = sorted(asteroids_sorted[key], key=lambda asteroid: asteroid[0])[0]
            asteroids_sorted[key].remove(destroyed)
            shotdown += 1
            #print("The {} asteroid to be vaporized is at {}".format(shotdown, (destroyed[2], destroyed[1])))
            if shotdown == 200:
                print("Part 2: The {} asteroid to be vaporized is at {}, giving answer {}".format(shotdown, (destroyed[2], destroyed[1]), 100*destroyed[2]+destroyed[1]))
                sys.exit()

