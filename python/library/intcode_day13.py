
import numpy as nd
import queue

# IntComp
#
# Parameters:
#
# 'prog'            the code to execute
# 'debug'           flag produces debug output
# 'nonblocking'     flag delivers -1 on input if there is no input on queue (otherwise it is blocking)
# 
class IntComp:

    FINISHED = 0
    NOT_FINISHED = -99

    def __init__(self, prog, debug = False, nonblocking = False):

        # Set debug flag
        self._debug = debug
        self._nonblocking = nonblocking

        # Set state
        self.pos = 0
        self.base_addr = 0
        self.curr_instr = None

        # Initialize memory to a large 0 array
        self.mem = nd.zeros(1000000, dtype=object)

        # Setup the input queue
        self.input_data = queue.Queue()

        # copy program into memory
        for i in range(0, len(prog)):
            self.mem[i] = prog[i]
        for i in range(len(prog), 1000000):
            self.mem[i] = '0'

    def clone(self):
        clone = IntComp([])
        clone.mem = list(self.mem)
        clone.pos = self.pos
        clone.base_addr = self.base_addr
        clone.curr_instr = self.curr_instr

        return clone

    # Internal debug output function
    def _dump(self, str):
        if self._debug:
            print(str)

    # Parse next instruction
    def _parse_instr(self):
        self.curr_instr = self.mem[self.pos].zfill(5)
        self.opcode = int(self.curr_instr[3:5])
        self._dump("CURRENT (pos {}): {}, MEM: {}".format(self.pos, self.curr_instr, self.mem[self.pos+1:self.pos + 4]))

    def add_input(self, input):
        self.input_data.put(input)

    def idle(self):
        return self._nonblocking and self.input_data.empty()

    def _next_input(self):
        if self._nonblocking and self.input_data.empty():
            return -1
            
        return self.input_data.get()

    def _param(self, param_num, is_write_address=False):
        if param_num == 1:
            mode = self.curr_instr[2]
        elif param_num == 2:
            mode = self.curr_instr[1]
        elif param_num == 3:
            mode = self.curr_instr[0]

        # the third parameter is always has an immediate parameter
        if is_write_address:
            if mode == '2':
                return self.base_addr + int(self.mem[self.pos+param_num])
            else:
                return int(self.mem[self.pos+param_num])
                        
        if mode == '0':
            return int(self.mem[int(self.mem[self.pos+param_num])])
        if mode == '1':
            return int(self.mem[self.pos+param_num])
        if mode == '2':
            return int(self.mem[self.base_addr + int(self.mem[self.pos+param_num])])
        

    def run(self, output_func, input_func):

        while True:

            # load the instruction (fill with zeros) and get param mode
            self._parse_instr()

            # Validate opcode
            if self.opcode == 99:
                return (IntComp.FINISHED, int(self.mem[0]))
            elif self.opcode == 1:
                self._dump('[1 ADD] mem[{}] <- {} + {}'.format(self._param(3, True), self._param(1), self._param(2)))
                self.mem[self._param(3, True)] = str(self._param(1) + self._param(2))
                self.pos += 4
            elif self.opcode == 2:
                self._dump('[2 MUL] mem[{}] <- {} * {}'.format(self._param(3, True), self._param(1), self._param(2)))
                self.mem[self._param(3, True)] = str(self._param(1) * self._param(2))
                self.pos += 4
            elif self.opcode == 3:
                input_val = input_func()
                self._dump('[3 IN] mem[{}] <- {}'.format(self._param(1, True), input_val))
                self.mem[self._param(1, True)] = str(input_val)
                self.pos += 2
            elif self.opcode == 4:
                self._dump('[4 OUT] Printing {}'.format(self._param(1)))
                output_func(self._param(1))
                self.pos += 2
                return (IntComp.NOT_FINISHED, -1)
            elif self.opcode == 5:
                if self._param(1) != 0:
                    self._dump('[5 JIT] {} != 0 => pos <- {}'.format(self._param(1), self._param(2)))
                    self.pos = self._param(2)
                else:
                    self._dump('[5 JIT] {} == 0 => NOOP '.format(self._param(1)))
                    self.pos += 3
            elif self.opcode == 6:
                if self._param(1) == 0:
                    self._dump('[6 JIF] pos <- {}'.format(self._param(2)))
                    self.pos = self._param(2)
                else:
                    self._dump('[6 JIF] NOOP ')
                    self.pos += 3
            elif self.opcode == 7:
                if self._param(1) < self._param(2):
                    self._dump('[7 LT] {} < {}? YES => mem[{}] <- 1'.format(self._param(1), self._param(2), self._param(3, True)))
                    self.mem[self._param(3, True)] = '1'
                else:
                    self._dump('[7 LT] {} < {}? NO => mem[{}] <- 0'.format(self._param(1), self._param(2), self._param(3, True)))
                    self.mem[self._param(3, True)] = '0'
                self.pos += 4
            elif self.opcode == 8:
                if self._param(1) == self._param(2):
                    self._dump('[8 EQ] {} == {}? YES => mem[{}] <- 1'.format(self._param(1), self._param(2), self._param(3, True)))
                    self.mem[self._param(3, True)] = '1'
                else:
                    self._dump('[8 EQ] {} == {}? NO => mem[{}] <- 0'.format(self._param(1), self._param(2), self._param(3, True)))
                    self.mem[self._param(3, True)] = '0'
                self.pos += 4
            elif self.opcode == 9:
                self._dump('[9 BASE] base_addr <- {} + {} = {}'.format(self.base_addr, self._param(1), self.base_addr + self._param(1)))
                self.base_addr += self._param(1)
                self.pos += 2
            else: 
                raise Exception("Unknown Opcode ({}) detected at position {}".format(self.opcode, self.pos))
