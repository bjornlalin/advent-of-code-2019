import sys
import numpy as nd

# Part 1 check
def valid(pwd):
    double = False
    last = -1
    for c in pwd:
        if int(c) < last:
            return False
        if int(c) == last:
                double = True
            
        last = int(c)
    
    return double

# Part 2 check
def valid2(pwd):
    double = False
    num_same = 1
    last = -1
    for c in pwd:

        if int(c) < last:
            return False

        if int(c) == last:
            num_same += 1
        else:
            if num_same == 2:
                double = True
            num_same = 1
            
        last = int(c)

    # Final letter needs to be considered as well
    if num_same == 2:
        double = True

    return double

def solve(low, high):
    print("Solving puzzle...")

    num_pwd_1 = 0
    num_pwd_2 = 0
    for pwd in range(low, high + 1):
        num_pwd_1 += valid(str(pwd))
        num_pwd_2 += valid2(str(pwd))

    print("Part 1: {}".format(num_pwd_1))
    print("Part 2: {}".format(num_pwd_2))

def test():
    print("Running tests...")

    test_part1()
    test_part2()

def test_part1():
    for (input, expected) in [("111111", True),("223450", False),("123789", False)]:
        print("{}: received {}, expected {}".format(input, valid(input), expected))

def test_part2():
    for (input, expected) in [("111111", False),("111122", True),("112222", True)]:
        print("{}: received {}, expected {}".format(input, valid2(input), expected))

test()
solve(265275, 781584)
