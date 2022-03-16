class Disassembler:
    def __init__(self):
        self.instruction_size = 4
        self.commands_dict = {
            0x01: 'print_str',
            0x02: 'print_int',
            0x03: 'scan_int',
            0x04: 'mov',
            0x05: 'add',
            0x06: 'sub',
            0x07: 'cmp',
            0x08: 'je',
            0x09: 'jmp',
            0x0A: 'jg',
            0x0B: 'call',
            0x0C: 'ret',
            0x0D: 'push',
            0x0E: 'pop',
            0x0F: 'stack_mov',
            0xFF: 'stop'
        }
        self.args_num = {
            'print_str': 1,
            'print_int': 1,
            'scan_int': 1,
            'mov': 2,
            'add': 2,
            'sub': 2,
            'cmp': 2,
            'je': 1,
            'jmp': 0,
            'jg': 1,
            'call': 1,
            'ret': 0,
            'push': 1,
            'pop': 1,
            'stack_mov': 2,
            'stop': 0
        }

        # команды, работающие с переменными
        self.vars_commands = tuple(self.commands_dict.values())[:7]
        self.vars_commands += tuple(self.commands_dict.values())[12:15]

        # команды, работающие с метками
        self.labels_commands = tuple(self.commands_dict.values())[7:11]

        self.code_lines = []
        self.byte_code = bytearray()
        self.var_section = bytearray()
        self.instructions = []

        # словарь, сопоставляющий адресу  ячейки в памяти
        # имя переменной (в том числе константы)
        self.variables = {}

        # словарь, сопоставляющий адресу ячейки в памяти имя метки
        self.labels = {}

    def process_variables(self) -> None:
        """
        Находит все уникальные адреса переменных в памяти и сопоставляет каждому
        его имя, строку или число (если константа). Сначала в памяти
        располагаются строки, потом - остальные переменные.
        :return: None
        """
        addresses = []
        var_addresses = []

        for command, receiver, source in self.instructions:
            if command == 'print_str':
                str_end = source
                while self.var_section[str_end] != 0x00:
                    str_end += 1
                string = self.var_section[source:str_end].decode('utf-8')
                self.variables[source] = f'"{string}"'
            elif command in self.vars_commands:
                addresses.append(source)
                if self.args_num[command] > 1:
                    addresses.append(receiver)
                    var_addresses.append(receiver)

        # определяем константы
        addresses = set(addresses)
        var_addresses = set(var_addresses)
        constant_addresses = addresses - var_addresses

        # добавляем имена переменных
        var_number = 1
        for address in var_addresses:
            self.variables[address] = f'var_{var_number}'
            var_number += 1

        # добавляем константы
        for address in constant_addresses:
            value = int.from_bytes(self.var_section[address:address + 4], 'big')
            self.variables[address] = value

    def process_labels(self) -> None:
        """
        Находит в коде все адреса меток и каждому сопоставляет имя метки
        (сгенерированное).
        :return: None
        """
        label_addresses = []

        for command, _, source in self.instructions:
            if command in self.labels_commands:
                label_addresses.append(source)

        # добавляем имена меток
        label_number = 1
        for address in set(label_addresses):
            self.labels[address] = f'label_{label_number}'
            label_number += 1

    def process_instructions(self) -> None:
        """
        Преобразует каждую строчку с инструкцией в 4 байта.
        :return: None
        """
        self.code_lines.append('start:')
        label_places = [((address - len(self.var_section)) // 4, address) for
                        address in self.labels.keys()]
        label_places.sort()

        place = 0
        for i, (command, receiver, source) in enumerate(self.instructions):
            # если пришло время ставить метку, делаем это
            if place < len(label_places) and i == label_places[place][0]:
                address = label_places[place][1]
                self.code_lines.append(self.labels[address] + ':')
                place += 1

            command_str = '\t' + command
            if command in self.vars_commands:  # работаем с переменными
                if self.args_num[command] == 1:
                    command_str += ' ' + self.variables[source]
                else:
                    command_str += ' ' + self.variables[receiver] + ', ' + \
                                   str(self.variables[source])
            elif command in self.labels_commands:  # работаем с метками
                command_str += ' ' + self.labels[source]
            self.code_lines.append(command_str)

    def get_asm_code(self, input_filename: str, output_filename: str) -> None:
        """
        Преобразует байт-код в ассемблерный код.
        :param input_filename: имя входного файла с байт-кодом
        :param output_filename: имя выходного файла с ассемблерным кодом
        :return: None
        """
        with  open(input_filename, 'rb') as byte_code:
            self.byte_code = bytearray(byte_code.read())

        start = int.from_bytes(self.byte_code[:self.instruction_size], 'big')
        self.var_section = self.byte_code[:start]

        code_section = self.byte_code[start:]
        for i in range(0, len(code_section), self.instruction_size):
            instruction = code_section[i: i + self.instruction_size]
            command = self.commands_dict[instruction[0]]
            receiver = instruction[1]
            source = int.from_bytes(instruction[2:], 'big')
            self.instructions.append((command, receiver, source))

        self.process_variables()
        self.process_labels()
        self.process_instructions()

        with open(output_filename, 'w', encoding='utf-8') as code:
            code.write('\n'.join(self.code_lines))
