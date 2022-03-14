class SimpleVM:
    def __init__(self):
        self.instruction_size = 4
        self.memory = bytearray()

        # регистры виртуальной машины:
        self.EIP = 0
        self.EAX = 0
        self.EBX = 0
        self.ECX = 0
        self.EDX = 0
        self.ESP = 0

        # флаги регистр флагов
        self.ZF = False  # равенство
        self.LF = False  # меньше

        self.commands_dict = {
            0x01: self.print_str,
            0x02: self.print_int,
            0x03: self.scan_int,
            0x04: self.mov,
            0x05: self.add,
            0x06: self.sub,
            0x07: self.cmp,
            0x08: self.je,
            0x09: self.jmp,
            0x0A: self.jg,
            0x0B: self.call,
            0x0C: self.ret,
            0x0D: self.push,
            0x0E: self.pop,
            0x0F: self.stack_mov,
        }

        # команды, работающие с метками
        self.labels_commands = tuple(self.commands_dict.keys())[7:9]

    def print_str(self) -> None:
        """
        Выводит строку на экран.
        :return: None
        """
        self.EAX = self.ECX = int.from_bytes(
            self.memory[self.EIP + 2:self.EIP + 4], 'big')
        while self.memory[self.ECX] != 0x00:
            self.ECX += 1
        print(self.memory[self.EAX:self.ECX].decode('utf-8'))

    def print_int(self) -> None:
        """
        Выводит целое число на экран.
        :return: None
        """
        self.EAX = int.from_bytes(self.memory[self.EIP + 2:self.EIP + 4], 'big')
        print(int.from_bytes(self.memory[self.EAX:self.EAX + 4], 'big'))

    def scan_int(self) -> None:
        """
        Считывает целое число со стандортного входа.
        :return: None
        """
        self.EAX = int.from_bytes(self.memory[self.EIP + 2:self.EIP + 4], 'big')
        self.memory[self.EAX:self.EAX + 4] = int(input()).to_bytes(4, 'big')

    def mov(self) -> None:
        """
        Помещает значение из переменной источника в переменную приёмника.
        :return: None
        """
        self.EAX = int(self.memory[self.EIP + 1])
        self.ECX = int.from_bytes(self.memory[self.EIP + 2:self.EIP + 4], 'big')
        self.memory[self.EAX:self.EAX + 4] = self.memory[self.ECX:self.ECX + 4]

    def parse_ints(self) -> None:
        """
        Читает два числа (приёмник и источник) из памяти и помещает значения в
        регистры EBX и EDX
        :return: None
        """
        self.EAX = int(self.memory[self.EIP + 1])
        self.ECX = int.from_bytes(self.memory[self.EIP + 2:self.EIP + 4], 'big')
        self.EBX = int.from_bytes(self.memory[self.EAX:self.EAX + 4], 'big')
        self.EDX = int.from_bytes(self.memory[self.ECX:self.ECX + 4], 'big')

    def add(self) -> None:
        """
        Прибавляет значение из переменной источника к переменной приёмника.
        :return: None
        """
        self.parse_ints()
        self.EBX += self.EDX
        self.memory[self.EAX:self.EAX + 4] = self.EBX.to_bytes(4, 'big')

    def sub(self) -> None:
        """
        Отнимает значение из переменной источника от переменной приёмника.
        :return: None
        """
        self.parse_ints()
        self.EBX -= self.EDX
        self.memory[self.EAX:self.EAX + 4] = self.EBX.to_bytes(4, 'big')

    def cmp(self) -> None:
        """
        Сравнивает значения переменной источника и переменной приёмника.
        :return: None
        """
        self.parse_ints()
        self.ZF = (self.EBX == self.EDX)
        self.LF = (self.EBX < self.EDX)

    def je(self) -> None:
        """
        Если выполнено равенство, перемещается по метке.
        :return: None
        """
        if self.ZF:
            self.jmp()

    def jmp(self) -> None:
        """
        Перемещается по метке.
        :return: None
        """
        self.EIP = int.from_bytes(self.memory[self.EIP + 2:self.EIP + 4], 'big')
        self.EIP -= 4

    def jg(self) -> None:
        """
        Если выполнено неравенство "больше", перемещается по метке.
        :return: None
        """
        if not (self.ZF or self.LF):
            self.jmp()

    def call(self) -> None:
        """
        Перемещается по метке, вызывая функцию.
        :return: None
        """
        self.ESP -= 4
        self.memory[self.ESP:self.ESP + 4] = self.EIP.to_bytes(4, 'big')
        self.EIP = int.from_bytes(self.memory[self.EIP + 2:self.EIP + 4], 'big')
        self.EIP -= 4

    def ret(self) -> None:
        """
        Команда возврата из функции.
        :return: None
        """
        self.EIP = int.from_bytes(self.memory[self.ESP:self.ESP + 4], 'big')
        self.ESP += 4

    def push(self) -> None:
        """
        Кладёт значение на стек.
        :return: None
        """
        self.ESP -= 4
        self.EAX = int.from_bytes(self.memory[self.EIP + 2:self.EIP + 4], 'big')
        self.memory[self.ESP:self.ESP + 4] = self.memory[self.EAX:self.EAX + 4]

    def pop(self) -> None:
        """
        Снимает значение со стека.
        :return: None
        """
        self.EAX = int.from_bytes(self.memory[self.EIP + 2:self.EIP + 4], 'big')
        self.memory[self.EAX:self.EAX + 4] = self.memory[self.ESP:self.ESP + 4]
        self.ESP += 4

    def stack_mov(self) -> None:
        """
        Помещает в переменную значение из стека. Место в стеке задаётся сдвигом
        относительно регистра ESP.
        :return: None
        """
        self.parse_ints()
        self.ECX = self.memory[self.ESP + self.EDX:self.ESP + self.EDX + 4]
        self.memory[self.EAX:self.EAX + 4] = self.ECX

    def run_program(self, filename: str, size: int = None) -> None:
        """
        Выполняет программу по байт-коду
        :param filename: название файла с байт-кодом
        :param size: память, выделяемая под программу
        :return: None
        """
        with  open(filename, 'rb') as byte_code:
            self.memory = bytearray(byte_code.read())
        if size is None:
            size = len(self.memory)
        if len(self.memory) > size:
            Exception('Выделяемой памяти не хватает')
        self.memory.extend(b'\x00' * (size - len(self.memory)))

        self.EIP = int.from_bytes(self.memory[:self.instruction_size], 'big')
        self.ESP = size
        while True:
            if self.memory[self.EIP] == 0xFF:
                # завершить выполнение
                break
            elif self.memory[self.EIP] in self.commands_dict.keys():
                self.commands_dict[self.memory[self.EIP]]()
            else:
                print(f'Неожиданная команда {self.memory[self.EIP]:02x}')
                break
            self.EIP += self.instruction_size
