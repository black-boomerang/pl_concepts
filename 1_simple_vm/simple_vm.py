class SimpleVM:
    def __init__(self):
        self.instruction_size = 4
        self.memory = bytes()
        self.IP = 0
        self.EAX = 0
        self.ECX = 0

    def run_program(self, filename):
        with  open(filename, 'rb') as byte_code:
            self.memory = byte_code.read()

        self.IP = int.from_bytes(self.memory[:self.instruction_size], 'big')
        while True:
            if self.memory[self.IP] == 0x01:
                # напечатать строку
                self.EAX = self.ECX = int.from_bytes(
                    self.memory[self.IP + 2:self.IP + 4], 'big')
                while self.memory[self.ECX] != 0x00:
                    self.ECX += 1
                print(self.memory[self.EAX:self.ECX].decode('utf-8'))
            elif self.memory[self.IP] == 0xFF:
                # завершить выполнение
                break
            else:
                print(f'Unexpected command {self.memory[self.IP]:02x}')
                break
            self.IP += self.instruction_size
