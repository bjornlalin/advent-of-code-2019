import sys

# Generates the path as a list of coordinate tuples (x,y,manhattan-distance)
# by following the instructions in the input
def path(steps):
    path = []
    x = 0
    y = 0
    for step in steps:
        direction = step[0]
        num_steps = int(step[1:])
        #print('Moving {} steps {}'.format(num_steps, direction))
        for step in range(0, num_steps):
            if direction == 'R':
                x += 1
            elif direction == 'U':
                y += 1
            elif direction == 'D':
                y -= 1
            elif direction == 'L':
                x -= 1
            
            path.append((x,y,abs(x) + abs(y)))
    
    return path

# Create all coordinates on the path for each route description from the input
path1 = path(sys.stdin.readline().strip('\n').split(','))
path2 = path(sys.stdin.readline().strip('\n').split(','))

# Find the intersection of the two sets
intersections = list(set(path1).intersection(set(path2)))

# Sort by manhattan distance to have the solution at index 0
intersections.sort(key = lambda x : x[2])

print("Part 1: the closest manhattan distance to where the wires intersect is {}".format(intersections[0][2]))

# Part 2 solution
# 
# Find the first index of each intersection in each path and calculate the sum.
# Keep the smallest one.
best = 1000000
for intersect in intersections:
    sum = path1.index(intersect) + path2.index(intersect) + 2
    if sum < best:
        best = sum

print("Part 2: the shortest total number of steps to where the wires intersect is {}".format(best))
