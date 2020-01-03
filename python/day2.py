import sys

def execute(prog, noun, verb):

    # create a copy of prog and set input
    mem = prog[:]
    mem[1] = noun
    mem[2] = verb

    # Set initial mem position
    pos = 0

    # Execute instructions
    while True:
        if mem[pos] == 1:
            mem[mem[pos+3]] = mem[mem[pos+1]] + mem[mem[pos+2]]
        elif mem[pos] == 2:
            mem[mem[pos+3]] = mem[mem[pos+1]] * mem[mem[pos+2]]
        elif mem[pos] == 99:
             return mem[0]
        
        pos += 4

########################
# Here execution starts
########################

for line in sys.stdin:

    # load prog
    prog = line.replace(' ', '').replace('\n', '').split(',')
    prog = [int(x) for x in prog]

    # Part 1
    print("Part 1: After halting program, position 0 contains {}".format(execute(prog, 12, 2)))

    # Part 2
    goal = 19690720
    for noun in range(0, 100):
        for verb in range(0, 100):
            if execute(prog, noun, verb) == goal:
                print("Part 2: With input noun={} and verb={} the output is {}. The requested answer (100 * noun + verb) is {}".format(noun, verb, goal, (100*noun + verb)))
    