import sys
import re
import numpy as nd
    
base_phases = [1, 0, -1, 0]

def to_i_a(line):
    i_a = []
    for c in line:
        i_a.append(int(c))

    return i_a

def filter(i_a, index):
    # Repeated pattern (subtract the number of leading 0's for the offset)
    pattern = nd.repeat(base_phases, index+1)[0:len(i_a)]
    n_tiles = int(((len(i_a) / len(pattern)) - index))

    if (len(i_a) - index) % len(pattern) == 0:
        n_tiles = int((len(i_a) - index) / len(pattern))
    else:
        n_tiles = int((len(i_a) - index) / len(pattern)) + 1

    # Paste the repeated pattern together
    tiles = nd.tile(pattern, n_tiles)

    # Add the initial 0's at the beginning and concatenate to exact length
    start = nd.zeros(index, dtype = int)
    return nd.append(start, tiles).tolist()[0:len(i_a)]

def apply_filter(input, filter):
    sum = 0
    for i in range(0, len(input)):
        sum += input[i] * filter[i]
    
    if sum < 0:
        sum *= -1
    
    return sum % 10

def phase(input):
    output = []
    for i in range(0, len(input)):
        f = filter(input, i)
        output.append(apply_filter(input, f))

    return output

def solve(line):
    input = to_i_a(line)
    for _ in range(0, 100):
        input = phase(input)
    print(''.join(map(lambda i : str(i), input[0:8])))

# Read input and create data structures
for line in sys.stdin:
    solve(line)
