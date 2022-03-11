from assembler import Assembler
from simple_vm import SimpleVM

if __name__ == '__main__':
    vm = SimpleVM()
    asm = Assembler()
    asm.get_byte_code('fibonacci.asm', 'fibonacci.byte')
    vm.run_program('fibonacci.byte')
