import sys
import library.intcode_day9 as comp

def solve(line):
    program = line.replace(' ', '').replace('\n', '').split(',')
    c = comp.IntComp(program, debug=False)
    while(c.run(lambda output : print(output))[0] != comp.IntComp.FINISHED):
        True

def solve_with_input(line, input):
    program = line.replace(' ', '').replace('\n', '').split(',')
    c = comp.IntComp(program, debug=False)
    c.add_input(input)

    # Execute the program in a loop until it provides no more output and reports 
    # that is has finished.
    stopped = False
    while not stopped:
        result = c.run(lambda output : print(output))
        if result[0] == comp.IntComp.FINISHED:
            stopped = True
            print('Final result code from program: {}'.format(result[1]))

def test():

    print('Test 1 (expect output "1125899906842624"):')
    solve('104,1125899906842624,99')

    print('Test 2 (expect output a 16-digit number:')
    solve('1102,34915192,34915192,7,4,7,99,0')

    print('Test 3 (expect output "109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99"):')
    solve('109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99')

# Run unit tests
test()

# Run on actual input
for line in sys.stdin:
    print("Part 1: executing")
    solve_with_input(line, '1')
    print("Part 2: executing")
    solve_with_input(line, '2')