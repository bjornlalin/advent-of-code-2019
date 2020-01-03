import sys
import numpy as nd

DEBUG = False

# Debug output
def _print(str):
    if DEBUG:
        print(str)

# Debug output
def _printGrid(grid):
    if DEBUG:
        for row in range(0,5):
            for col in range(0, 5):
                if grid[row, col] == 1:
                    print('#', end='')
                elif grid[row, col] == -1:
                    print('?', end='')
                else:
                    print('.', end='')
            print()

# Number of adjacent bugs, not considering
# any levels (as needed by part 1 and re-used
# by part 2)
def nAdjacent(grid, row, col):
    n = 0
    if row > 0 and grid[row-1,col] == 1:
        n += 1
    if row < 4 and grid[row+1,col] == 1:
        n += 1
    if col > 0 and grid[row,col-1] == 1:
        n += 1
    if col < 4 and grid[row,col+1] == 1:
        n += 1
    return n

# Create a hash (bitmask) from array
def hash(grid):
    key = 0
    for pos in range(0,25):
        if grid[int(pos/5),pos%5] == 1:
            key += 2**pos

    return key

# Create a numpy 5x5 array from bitmask
def unhash(key):
    grid = nd.zeros((5,5), dtype=int)
    for pos in range(0,25):
        if (2**pos) & key:
            grid[int(pos/5),pos%5] = 1
        else:
            grid[int(pos/5),pos%5] = 0

    return grid

# Count number of bugs on a grid
def nBugs(key):
    n = 0
    for pos in range(0,25):
        if (2**pos) & key:
            n += 1
    return n

# create a numpy 5x5 array from bitmask with middle position as -1
def unhash2(key):
    grid = unhash(key)
    grid[2,2] = -1
    return grid

#
# Part 1 
#############################

# Generate next grid from a grid
def step1(grid):
    nextgrid = nd.zeros((5,5), dtype=object)
    for row in range(0,5):
        for col in range(0,5):
            if grid[row,col] == 1:
                if nAdjacent(grid, row, col) == 1:
                    nextgrid[row, col] = 1
                else:
                    nextgrid[row,col] = 0
            if grid[row,col] == 0:
                if nAdjacent(grid, row, col) == 1 or nAdjacent(grid, row, col) == 2:
                    nextgrid[row, col] = 1
                else:
                    nextgrid[row,col] = 0
    return nextgrid

def solve1(grid):

    # Keep track of which grids we have seen
    seen = {hash(grid)}

    while(True):
        # Take a turn and generate next hash
        grid = step1(grid)
        key = hash(grid)

        # Check if we have already seen this configuration, then we're done
        if key in seen:
            print("Part 1: {}".format(key))
            break
        # Otherwise remember it for later
        else:
            seen.add(key)

#
# Part 2
#############################

# Part 2: take a turn considering same as well as inner and outer levels
def step2(sq, sq_inner, sq_outer):

    # Clean next state
    next_sq = nd.zeros((5,5), dtype=int)
    
    # Iterate square
    for row in range(0, 5):
        for col in range(0, 5):
            
            # Center is '?'
            if row == 2 and col == 2:
                next_sq[row, col] = -1
                continue

            # Same level adjacent
            n_adj = nAdjacent(sq, row, col)

            # outer level adjavent
            if row == 0:
                n_adj += nd.sum(sq_outer[1,2])
            if row == 4:
                n_adj += nd.sum(sq_outer[3,2])
            if col == 0:
                n_adj += nd.sum(sq_outer[2,1])
            if col == 4:
                n_adj += nd.sum(sq_outer[2,3])

            # Inner level adjacent
            if row == 1 and col == 2:
                n_adj += nd.sum(sq_inner[0,:])
            if row == 3 and col == 2:
                n_adj += nd.sum(sq_inner[4,:])
            if col == 1 and row == 2:
                n_adj += nd.sum(sq_inner[:,0])
            if col == 3 and row == 2:
                n_adj += nd.sum(sq_inner[:,4])
            
            if sq[row,col] == 1:
                if n_adj == 1:
                    next_sq[row, col] = 1
                else:
                    next_sq[row,col] = 0

            if sq[row,col] == 0:
                if n_adj == 1 or n_adj == 2:
                    next_sq[row, col] = 1
                else:
                    next_sq[row,col] = 0
    
    return hash(next_sq)

def solve2(grid, minutes):
    # keep track of levels
    grid[2,2] = -1
    grids = { 0 : hash(grid) }

    for min in range(0, minutes):

        # Collect all results from a turn in this map
        nextgrids = {}

        # Get all levels
        levels = sorted(grids.keys())
        levels = [levels[0]-1] + levels + [levels[len(levels)-1]+1]

        for level in levels:

            if level in grids.keys():
                grid = grids[level]
            else:
                grid = 0

            if (level-1) in grids.keys():
                outer = grids[level-1]
            else:
                outer = 0

            if (level+1) in grids.keys():
                inner = grids[level+1]
            else:
                inner = 0
            
            sq = unhash2(grid)
            sq_inner = unhash2(inner)
            sq_outer = unhash2(outer)

            # Calculate next grid
            nextgrids[level] = step2(sq, sq_inner, sq_outer)

        grids = nextgrids

    # Debug output of final configuration
    _print('------------------------------')
    _print('After {} min: '.format(min))
    _print('------------------------------')
    for level in sorted(grids.keys()):
        _print('level {}:'.format(level))
        _printGrid(unhash2(grids[level]))
        _print('')
    _print('')
    _print('')

    n = 0
    for key in grids.values():
        n += nBugs(key)

    print('Part 2: there are {} bugs across all levels after {} minutes'.format(n, minutes))
    
# Original data
original = nd.zeros((5,5), dtype=object)

# Read data into grid from stdin
row = 0
for line in sys.stdin:
    col = 0
    for c in line.replace('\n','').strip('\n'):
        if c == '#':
            original[row, col] = 1
        else:
            original[row, col] = 0
        col += 1
    row += 1

# Solve
solve1(nd.copy(original))
solve2(nd.copy(original), 200)
