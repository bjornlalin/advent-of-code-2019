import os 
import sys
import library.intcode_day9 as comp

script_part1 = """NOT C T
NOT A J
OR  J T
NOT T J
OR  D J
AND T J
WALK
"""

script_part2 = """NOT C J 
AND D J 
AND H J
NOT B T 
AND D T 
OR T J
NOT A T 
OR T J
RUN
"""

def _debug(str):
    if False:
        print(str)

class SpringDroid:

    _awaits_command = True
    _command = ''
    _output = ''

    def __init__(self, program, script, interactive=False):
        self.intcode = comp.IntComp(list(program), debug=False)
        self._interactive = interactive
        self._script = script

    def output(self, charcode):
        if self._awaits_command:
            if charcode == 10:
                self.get_script()
            else:
                self._command += chr(charcode)
        else:
            if charcode > 255:
                print("Hull damage: {}".format(charcode))
            else:
                self._output += chr(charcode)
                if charcode == 10:
                    print(self._output)

    def get_script(self):
        if self._interactive:
            script = self.editor()
        else:
            script = self._script

        # We expect an output now instead of input
        self._awaits_command = False

        # Pass program to computer as ascii codes
        for c in script:
            self.intcode.add_input(ord(c))

    def editor(self):
        buffer = ''
        while True:
            line = input("script> ")
            buffer += line
            buffer += '\n'
            if line.startswith('WALK') or line.startswith('RUN'):
                break
        
        return buffer

    def run(self, sprintscript):
        stopped = False
        while not stopped:
            status = self.intcode.run(self.output)
            if status[0] == comp.IntComp.FINISHED:
                stopped = True

def part1(line):
    program = line.replace(' ', '').replace('\n', '').split(',')
    robot = SpringDroid(program, script_part1)
    robot.run(None)

def part2(line):
    program = line.replace(' ', '').replace('\n', '').split(',')
    robot = SpringDroid(program, script_part2)
    robot.run(None)

# Fetch input and call solve routine. We need to do this using
# a file instead of piping stdin, since I solved this puzzle manually
dir_path = os.path.dirname(os.path.realpath(__file__))
f = open("{}/../input/day21.in".format(dir_path), "r")

for line in f:
    part1(line)
    part2(line)

##################
# Program Part 1
##################
#
# This was solved manually: 
# 
# (!C or !A) and (D)
# 
# The corresponding program is:
# 
# NOT C T
# NOT A J
# OR  J T  T = !A or !C
# NOT T J
# OR  D J
# AND T J
#
#    @                     @                      @   @
#   @ @                   @ @                    @ @ @ @
#  @   @                 @   @                  @   @   @
#  ####X#########      ##### #  #######      ###### # # X ####
#   ----                  ----                   ----
#
#                                            Cannot detect this 
#                                            with 4 steps look-
#                                            ahead anyway
#


##################
# Program Part 2
##################
#
# This was solved manually: 
# 
# (!C or !B or !A) and (D) and (H)
# 
# The corresponding program is:
# 
# NOT C T
# NOT A J
# OR  J T  T = !A or !C
# NOT B J
# OR  J T  T = !A or !B or !C
# NOT T J
# OR D J
# AND T J
# AND H T
# AND T J
#
#    @                     @                      @   @
#   @ @                   @ @                    @ @ @ @
#  @   @                 @   @                  @   @   @
#  ####X#########      ##### #  #######      ###### # # X ####
#   ABCDEFGHI             ABCDEFGHI              ABCDEFGHI
#
#                                            Cannot detect this 
#                                            with 4 steps look-
#                                            ahead anyway
#
