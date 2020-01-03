import sys
import library.intcode_day9 as comp
import itertools

# We need to keep track of output from the computer
class State:
    def __init__(self):
        self.state = 0
    def setState(self, state):
        self.state = state

def calculate_thrust(program, phases):
    
    state = State()

    amps = []

    # Initialize all five amplifiers
    for phase in phases:
        amp = comp.IntComp(list(program))
        amp.add_input(phase)
        amps.append(amp)

    for amp in amps:
        amp.add_input(state.state)
        amp.run(lambda output: state.setState(output))
        
    return state.state

def calculate_thrust_part2(program, phases):

    state = State()

    amps = []

    # Initialize all five amplifiers
    for phase in phases:
        amp = comp.IntComp(list(program))
        amp.add_input(phase)
        amps.append(amp)

    stopped = False
    while not stopped:
        for amp in amps:
            amp.add_input(state.state) # pass input from last round
            return_code = amp.run(lambda output: state.setState(output))[0]
            if return_code == comp.IntComp.FINISHED:
                stopped = True

    return state.state

for line in sys.stdin:

    # Read program from stdin
    program = line.replace(' ', '').replace('\n', '').split(',')

    # Part 1: generate all possible phase settings and run the amplifiers
    max_thrust = 0
    for phases in itertools.permutations(['0', '1', '2', '3', '4']):
        max_thrust = max(max_thrust, calculate_thrust(list(program), phases))

    print("Part 1: max thrust is {}".format(max_thrust))
    
    # Part 1: generate all possible phase settings and run the amplifiers
    max_thrust = 0
    for phases in itertools.permutations(['5', '6', '7', '8', '9']):
        max_thrust = max(max_thrust, calculate_thrust_part2(list(program), phases))

    print("Part 2: max thrust is {}".format(max_thrust))
