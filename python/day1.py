import sys

# Fuel calculation for part 1
def fuel(mass):
    return max((mass / 3) - 2, 0)

# Fuel calculation with recursive ... fuel calculation
def fuel_rec(mass):

    # How much fuel do we need for this mass?
    f = fuel(mass)
   
    # Debug
    #print("mass {} needs fuel {}".format(mass, f))

    # Recursive stop condition
    if f == 0:
        return 0

    # Add fuel costs recursively
    return f + fuel_rec(f)

########################
# Here execution starts
########################

sum_1 = 0
sum_2 = 0

for line in sys.stdin:
    sum_1 += fuel(int(line))
    sum_2 += fuel_rec(int(line))

print("Part 1: total fuel used is {}".format(sum_1))
print("Part 2: total fuel used is {}".format(sum_2))
