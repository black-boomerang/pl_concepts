from disassembler import Disassembler

if __name__ == '__main__':
    disasm = Disassembler()
    disasm.get_asm_code('../assembler/fibonacci.byte', 'fibonacci.asm')

    disasm = Disassembler()
    disasm.get_asm_code('../assembler/fibonacci_recursive.byte',
                        'fibonacci_recursive.asm')
