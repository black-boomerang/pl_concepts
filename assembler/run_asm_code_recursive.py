from assembler import Assembler
from simple_vm import SimpleVM

if __name__ == '__main__':
    vm = SimpleVM()
    asm = Assembler()
    asm.get_byte_code('fibonacci_recursive.asm', 'fibonacci_recursive.byte')
    vm.run_program('fibonacci_recursive.byte', size=256)
