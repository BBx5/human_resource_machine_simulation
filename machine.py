import inspect

class Machine(object):
    """docstring for Machine"""
    def __init__(self, mem_size = 5):
        super(Machine, self).__init__()
        self.reset(mem_size)
        self.load_instruction_set()

    def load_inbox(self, input_file):
        for line in open(input_file):
            self._inbox.append(int(line))
        self._inbox.reverse()

    def reset(self, mem_size):
        self._inbox = []
        self._outbox = []
        self._pc = 0
        self._instructions = {}
        self._mem = [0]*mem_size
        self._reg0 = 0

    def load_instruction_set(self):
        for (n, f) in inspect.getmembers(self):
            if n.startswith("ins_"):
                self._instructions[n[4:]] = f

    def run(self, instructions):
        steps = 0
        while True:
            try:
                self._mexec(instructions[self._pc])
                self._pc += 1
                steps += 1
            except IndexError:
                print "Steps:", steps, ", Instructions:", len(instructions)
                return

    def _mexec(self, (instruction, args)):
        self._instructions[instruction](args)

    def ins_inbox(self, args):
        self._reg0 = self._inbox.pop()

    def ins_outbox(self, args):
        print self._reg0
        # self._outbox.append(reg0)

    def ins_add(self, args):
        self._reg0 += self._mem[args[0]]

    def ins_copyfrom(self, args):
        self._reg0 = self._mem[args[0]]

    def ins_copyto(self, args):
        self._mem[args[0]] = self._reg0

    def ins_sub(self, args):
        self._reg0 -= self._mem[args[0]]

    def ins_jump(self, args):
        self._pc  = args[0]
        self._pc -= 1

    def ins_jumpz(self, args):
        if self._reg0 == 0:
            self._pc = args[0]
            self._pc -= 1

    def ins_jumpn(self, args):
        if self._reg0 < 0:
            self._pc = args[0]
            self._pc -= 1


def parse(source_file):
    ret = []
    for line in open(source_file):
        segs = line.strip().split(" ")
        ins = segs[0].lower()
        args = map(int,segs[1:])
        ret.append((ins, args))
    return ret

def main(source_file, input_file, output_file):
    vm = Machine()
    vm.load_inbox(input_file)
    vm.run(parse(source_file))

if __name__ == '__main__':
    import sys
    main(sys.argv[1],sys.argv[2],"")
