import sys
import math
from collections import defaultdict

class Ingredient:
    def __init__(self, desc):
        token_1 = desc.strip().split(' ')[0].strip('')
        token_2 = desc.strip().split(' ')[1].strip('')
        self.material = token_2
        self.quantity = int(token_1)

    def __str__(self):
        return str(self.quantity) + " " + self.material
    
    def __repr__(self):
        return self.__str__()

class Reaction:
    def __init__(self, output, inputs):
        self.output = output
        self.inputs = inputs
    
    def __str__(self):
        result = ""
        for input in self.inputs:
            if result != "":
                result += ", "
            result += input.__str__()
        result += " => "
        result += self.output.__str__()
        return result
    
    def __repr__(self):
        return self.__str__()
    
# Store all reactions here
reactions = {}

# Store calculated material needs here
spillovers = defaultdict(int)
produced = defaultdict(int)

def _debug(str):
    if False:
        print(str)

# Solve recursively, taking spillovers into account
def produce(material, quantity):

    _debug('')
    _debug('requesting production of {} units of {}'.format(quantity, material))

    # This is the reaction to produce the 'needed' material
    reaction = reactions[material]

    _debug('Reaction to produce {} is {}'.format(material, reaction))

    # This is how much we need to produce after using any spillovers 
    # we have left from earlier production
    n_needed = quantity - spillovers[material]

    _debug('There are {} spillover {}, so we need to produce {} more'.format(spillovers[material], material, n_needed))

    # This many reactions we need to do to produce at least 'needed' material
    n_reactions = math.ceil(n_needed/reaction.output.quantity)
    n_produced = n_reactions * reaction.output.quantity
    n_spillover = n_produced - n_needed

    _debug('This requires {} reactions, producing {} units of {} and creating {} spillover'.format(n_reactions, n_produced, material, n_spillover))

    # Keep track of amount produced
    produced[material] = n_produced

    # Keep track of remaining spillovers
    spillovers[material] = n_spillover

    # Produce the input required
    for input in reaction.inputs:
        if input.material == 'ORE':
            _debug('We used {} ORE'.format((input.quantity * n_reactions)))
            produced["ORE"] += (input.quantity * n_reactions)
        else:
            produce(input.material, input.quantity * n_reactions)

def part1(n):
    produced.clear()
    spillovers.clear()
    produce('FUEL', n)
    return produced["ORE"]

def part2():
    total_fuel = 0
    low = 1
    high = 1_000_000_000

    # Exponentially seek a number larger than what we search
    while abs(high - low) > 1:
        n = int((high+low)/2)
        total_fuel = part1(n)

        print('{} fuels cost {} (searching in interval {}-{})'.format(str(n).zfill(10), str(total_fuel).zfill(13), low, high))

        if total_fuel > 1_000_000_000_000:
            high = n
        else:
            low = n

    return n-1

# Parse input
for line in sys.stdin:
    reaction = line.strip('\n').split('=>')

    output = Ingredient(reaction[1].strip())

    inputs = []
    for input_str in reaction[0].split(','):
        inputs.append(Ingredient(input_str))

    reactions[output.material] = Reaction(output, inputs)

print('Part 1: {} ORE required'.format(part1(1)))
print("Part 2: {}".format(part2()))
