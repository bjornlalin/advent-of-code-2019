import os 
import sys
import library.intcode_day9 as comp

def _debug(str):
    if False:
        print(str)

class Droid:

    def __init__(self, program):
        self.intcode = comp.IntComp(list(program), debug=False)
        self.text = ''

    def prompt(self, output):
        if output == 10:
            if self.text == "Command?":
                command = input("command> ")
                self.send_command(command)
            else:
                print(self.text)
            self.text = ''
        else:
            self.text += chr(output)

    def send_command(self, command):
        print("sending command: '{}'".format(command))
        for c in command:
            self.intcode.add_input(ord(c))
        self.intcode.add_input(10)

    def run(self):
        stopped = False
        while not stopped:
            status = self.intcode.run(self.prompt)
            if status[0] == comp.IntComp.FINISHED:
                stopped = True

# Fetch input and call solve routine. We need to do this using
# a file instead of piping stdin, since I solved this puzzle manually
dir_path = os.path.dirname(os.path.realpath(__file__))
f = open("{}/../input/day25.in".format(dir_path), "r")
for line in f:
    program = line.replace(' ', '').replace('\n', '').split(',')
    robot = Droid(program)
    robot.run()

f.close()

#
# Inventory to find password in security check:
#
# - cake
# - monolith
# - coin
# - mug
#