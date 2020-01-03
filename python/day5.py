import sys
import re
import library.intcode_day5 as intcode

# load prog
for line in sys.stdin:
    program = line.replace(' ', '').replace('\n', '').split(',')

    # Part 1 (we use list(...) to create a copy of the memory)
    print("Part 1: executing...")
    intcode.IntComp(list(program), debug=False).run(lambda: 1, lambda output : print(output))

    # Part 2 (we use list(...) to create a copy of the memory)
    print("Part 2: executing...")
    intcode.IntComp(list(program), debug=False).run(lambda: 5, lambda output : print(output))
