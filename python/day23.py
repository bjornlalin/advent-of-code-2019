import sys
from library.intcode_day9 import IntComp
import threading
import time

class NAT(threading.Thread):

    _first = True
    _deliveredY = set()

    def __init__(self, network):
        threading.Thread.__init__(self)
        self._network = network        
    
    def process(self, message):
        self.message = message

        # First message sent to NAT is the answer to part 1        
        if self._first:
            print('== [NAT] Part 1: {}'.format(self.message.y))
            self._first = False
        
        print('== [NAT] received message on address 255: {}'.format(message))

    def run(self):
        while True:
            time.sleep(10)
            if self._network.idle():
                print('== [NAT] detected idle network, sent input {} to nic with address {}'.format(self.message, 0))
                self._network.nics[0].comp.add_input(self.message.x)
                self._network.nics[0].comp.add_input(self.message.y)
                
                # First repeated message sent to address 0 is the answer to part 2
                if self.message.y in self._deliveredY:
                    print('== [NAT] Part 2: {}'.format(self.message.y))

                self._deliveredY.add(self.message.y)

            else:
                print('== [NAT] network not idle')
        
        

# Network message
class Message:
    def __init__(self, address, x, y):
        self.address = address
        self.x = x
        self.y = y

    def __str__(self):
        return "[addr: {}, X: {}, Y: {}]".format(self.address, self.x, self.y)

# NIC component
class NIC(threading.Thread):

    def _print(self, str):
        if self._debug:
            print(str)

    def __init__(self, program, address, interface, debug=False):

        threading.Thread.__init__(self)

        # set debug flag
        self._debug = debug

        # Initialize computer
        self.comp = IntComp(program, debug=False, nonblocking=True)

        # Network address
        self.address = address

        # State for sending messages
        self.n_out = 0
        self.address_out = -1
        self.x_out = -1
        self.y_out = -1

        # Interface to network (for sending messages over the network)
        self.interface = interface

        # Start thread
        self.threadID = address

        # Thread stop condition
        self.exit = False
    
    def out(self, value):
        if self.n_out % 3 == 0:
            self.address_out = value
        elif self.n_out % 3 == 1:
            self.x_out = value
        elif self.n_out % 3 == 2:
            self.y_out = value
            msg = Message(self.address_out, self.x_out, self.y_out)
            self._print('computer {} sends message {}'.format(self.address, msg))
            self.interface(msg)
        
        self.n_out += 1

    def send(self,x,y):
        self._print('computer {} received message ({},{})'.format(self.address, x, y))
        self.comp.add_input(x)
        self.comp.add_input(y)

    def boot(self):
        self._print('booting computer {}'.format(self.address))
        self.comp.add_input(self.address)

    def shutdown(self):
        self.exit = True

    def run(self):
        self._print('running computer {}'.format(self.address))
        stopped = False
        while not stopped and not self.exit:

            # Yield if no input available
            if self.comp.idle():
                time.sleep(0)

            status = self.comp.run(self.out)
            if status[0] == IntComp.FINISHED:
                self._print('NIC {} stopped'.format(self.address))
                stopped = True

class Network:

    _lastMessageTime = time.time()

    def __init__(self, program):

        self.nat = NAT(self)

        # Initialize all network interfaces
        self.nics = []
        for address in range(0, 50):
            self.nics.append(NIC(list(program), address, self.interface))

        # Boot all network interfaces        
        for nic in self.nics:
            nic.boot()

        for nic in self.nics:
            nic.start()

        self.nat.start()
    
    # Callback method for sending messages on the network
    def interface(self, message):
        self._lastMessageTime = time.time()

        if message.address == 255:
            self.nat.process(message)
        else:
            self.nics[message.address].send(message.x, message.y)

    # Check if networks are idle
    def idle(self):
        for nic in self.nics:
            if not nic.comp.idle():
                return False

        # If no messages on input queues and no messages sent for 10 sec, the network seems idle...
        return time.time() - self._lastMessageTime > 10

    # TODO: How do we kill the threads?
    def shutdown(self):
        for nic in self.nics:
            nic.shutdown()
        sys.exit()

def solve(line):
    program = line.replace(' ', '').replace('\n', '').split(',')
    Network(program)

for line in sys.stdin:
    solve(line)