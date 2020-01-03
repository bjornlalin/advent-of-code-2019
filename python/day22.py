import sys
import re

def _debug(str):
    if(True):
        print(str)

def dealIntoNewStack(deck):
    _debug("deal into new deck")
    newStack = []
    for i in range(len(deck)-1, -1, -1):
        newStack.append(deck[i])
    return newStack

def cutIntoN(deck, n):
    _debug("cut into {}".format(n))
    return deck[n:len(deck)] + deck[0:n]

def dealIntoIncrement(deck, incr):
    _debug("deal into increment {}".format(incr))
    newStack = [-1] * len(deck)
    pos = 0
    for i in range(0, len(deck)):
        newStack[pos] = deck[i]
        pos = (pos + incr) % len(deck)

    return newStack

def test():
    deck = list(range(0,10))

    test1 = dealIntoIncrement(deck, 7)
    test1 = dealIntoNewStack(test1)
    test1 = dealIntoNewStack(test1)
    print("Test 1: ", test1)

    test2 = cutIntoN(deck, 6)
    test2 = dealIntoIncrement(test2, 7)
    test2 = dealIntoNewStack(test2)
    print("Test 2: ", test2)

    test3 = dealIntoIncrement(deck, 7)
    test3 = dealIntoIncrement(test3, 9)
    test3 = cutIntoN(test3, -2)
    print("Test 3: ", test3)

    test4 = dealIntoNewStack(deck)
    test4 = cutIntoN(test4, -2)
    test4 = dealIntoIncrement(test4, 7)
    test4 = cutIntoN(test4, 8)
    test4 = cutIntoN(test4, -4)
    test4 = dealIntoIncrement(test4, 7)
    test4 = cutIntoN(test4, 3)
    test4 = dealIntoIncrement(test4, 9)
    test4 = dealIntoIncrement(test4, 3)
    test4 = cutIntoN(test4, -1)
    print("Test 4: ", test4)

#test()
#sys.exit()

deck = list(range(0, 10007))

for line in sys.stdin:

    if 'cut' in line:
        n = int(re.findall(r'[-]?\d+', line)[0])
        deck = cutIntoN(list(deck), n)
    elif 'increment' in line:
        incr = int(re.findall(r'\d+', line)[0])
        deck = dealIntoIncrement(list(deck), incr)
    elif 'new' in line:
        deck = dealIntoNewStack(list(deck))

print("Part 1: {}".format(deck.index(2019)))