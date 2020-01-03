class IntComp:

    pos = 0
    mem = None
    instr = None
    input_value = None
    _debug = False

    def __init__(self, prog, debug = False):
        self.mem = prog
        self._debug = debug

    def dump(self, str):
        if self._debug:
            print(str)

    def run(self, input_func, output_func):

        while True:

            # load the instruction (fill with zeros) and get param mode
            instr = self.mem[self.pos].zfill(5)
            opcode = int(instr[3:5])
            param_mode_1 = instr[2]
            param_mode_2 = instr[1]
            param_mode_3 = instr[0]

            # Validate opcode
            if opcode == 99:
                return int(self.mem[0])
            elif opcode in [1, 2]:
                param_1 = int(self.mem[self.pos+1]) if int(param_mode_1) else int(self.mem[int(self.mem[self.pos+1])])
                param_2 = int(self.mem[self.pos+2]) if int(param_mode_2) else int(self.mem[int(self.mem[self.pos+2])])
                param_3 = int(self.mem[self.pos+3])
                if opcode == 1:
                    self.dump('mem[{}] <- {} + {}'.format(param_3, param_1, param_2))
                    self.mem[param_3] = str(param_1 + param_2)
                if opcode == 2:
                    self.dump('mem[{}] <- {} * {}'.format(param_3, param_1, param_2))
                    self.mem[param_3] = str(param_1 * param_2)
                self.pos += 4
            elif opcode == 3:
                param_1 = int(self.mem[self.pos+1])
                input_val = input_func()
                self.dump('mem[{}] <- {}'.format(param_1, input_val))
                self.mem[param_1] = input_val
                self.pos += 2
            elif opcode == 4:
                param_1 = int(self.mem[self.pos+1]) if int(param_mode_1) else int(self.mem[int(self.mem[self.pos+1])])
                output_func(param_1)
                self.pos += 2
            elif opcode in [5, 6]:
                param_1 = int(self.mem[self.pos+1]) if int(param_mode_1) else int(self.mem[int(self.mem[self.pos+1])])
                param_2 = int(self.mem[self.pos+2]) if int(param_mode_2) else int(self.mem[int(self.mem[self.pos+2])])
                if opcode == 5:
                    if param_1 != 0:
                        self.dump('[5] pos <- {}'.format(param_2))
                        self.pos = param_2
                    else:
                        self.dump('[5] NOOP ')
                        self.pos += 3
                if opcode == 6:
                    if param_1 == 0:
                        self.dump('[6] pos <- {}'.format(param_2))
                        self.pos = param_2
                    else:
                        self.dump('[6] NOOP ')
                        self.pos += 3
            elif opcode in [7, 8]:
                param_1 = int(self.mem[self.pos+1]) if int(param_mode_1) else int(self.mem[int(self.mem[self.pos+1])])
                param_2 = int(self.mem[self.pos+2]) if int(param_mode_2) else int(self.mem[int(self.mem[self.pos+2])])
                param_3 = int(self.mem[self.pos+3])
                if opcode == 7:
                    if param_1 < param_2:
                        self.dump('[7] {} < {} => mem[{}] <- 1'.format(param_1, param_2, param_2))
                        self.mem[param_3] = 1
                    else:
                        self.dump('[7] {} >= {} => mem[{}] <- 0'.format(param_1, param_2, param_2))
                        self.mem[param_3] = 0
                if opcode == 8:
                    if param_1 == param_2:
                        self.dump('[8] {} == {} => mem[{}] <- 1'.format(param_1, param_2, param_2))
                        self.mem[param_3] = 1
                    else:
                        self.dump('[8] {} != {} => mem[{}] <- 0'.format(param_1, param_2, param_2))
                        self.mem[param_3] = 0
                self.pos += 4
            else: 
                raise Exception("Unknown Opcode ({}) detected at position {}".format(opcode, self.pos))
