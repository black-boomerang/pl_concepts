import re


class Assembler:
    def __init__(self):
        self.instruction_size = 4
        self.commands_dict = {
            'print_str': 0x01,
            'print_int': 0x02,
            'scan_int': 0x03,
            'mov': 0x04,
            'add': 0x05,
            'sub': 0x06,
            'cmp': 0x07,
            'je': 0x08,
            'jmp': 0x09,
            'jg': 0x0A,
            'call': 0x0B,
            'ret': 0x0C,
            'push': 0x0D,
            'pop': 0x0E,
            'stack_mov': 0x0F,
            'stop': 0xFF
        }
        # команды, работающие с переменными
        self.vars_commands = tuple(self.commands_dict.keys())[:7]
        self.vars_commands += tuple(self.commands_dict.keys())[12:15]

        # команды, работающие с метками
        self.labels_commands = tuple(self.commands_dict.keys())[7:11]

        self.code_lines = []
        self.byte_code = bytearray()

        # словарь, сопоставляющий имени переменной (в том числе константы)
        # адрес ячейки в памяти
        self.variables = {}

        # словарь, сопоставляющий имени метки адрес ячейки в памяти
        self.labels = {}

    def process_variables(self) -> None:
        """
        Находит все уникальные имена переменных в коде и сопоставляет каждому
        адрес в памяти. Сначала в памяти располагаются строки, потом - остальные
        переменные.
        :return: None
        """
        var_names = []

        strings_buffer = bytearray()
        str_num = 0
        for line_number, line in enumerate(self.code_lines):
            parts = re.split(r', |,\t| |\t', line)
            parts[0] = parts[0].lower()
            if parts[0] == 'print_str':
                # меняем строку на название переменной
                self.variables['$' + str(str_num)] = len(strings_buffer) + 4
                self.code_lines[line_number] = parts[0] + ' $' + str(str_num)
                str_num += 1

                # выделяем из кода печатаемую строку
                printed = re.findall(r'"(.*)"', line)[0].encode('utf-8')
                strings_buffer.extend(printed + b'\x00')

            elif parts[0] in self.vars_commands:
                var_names.extend(parts[1:])

        # дополняем нулями, чтобы длина была кратна 4
        strings_buffer += b'\x00' * (-len(strings_buffer) % 4)
        unique_names = list(set(var_names))

        # количество байт под переменные и IP
        data_size = len(strings_buffer) + len(unique_names) * 4 + 4

        # устанавливаем IP
        self.byte_code.extend(data_size.to_bytes(4, 'big'))
        # выделяем память под строки
        self.byte_code.extend(strings_buffer)
        # выделяем память под переменные
        for i, name in enumerate(unique_names):
            if name.isdigit():  # константа
                self.byte_code.extend(int(name).to_bytes(4, 'big'))
            else:  # переменная
                self.byte_code.extend(b'\x00' * 4)
            self.variables[name] = len(strings_buffer) + i * 4 + 4

    def process_labels(self) -> None:
        """
        Находит в коде все метки и для каждой вычисляет адрес инструкции,
        стоящей после этой метки. Пользуемся тем, что любая инструкция занимает
        4 байта.
        :return: None
        """
        data_size = len(self.byte_code)

        # в этой переменной считаем количество байт после байт-кода с данными
        bytes_num = 0
        for line in self.code_lines:
            parts = re.split(r', |,\t| |\t', line)
            if parts[0].endswith(':'):  # обработка метки
                label = parts[0].strip(':')
                self.labels[label] = data_size + bytes_num
            else:
                bytes_num += 4

    def process_instructions(self) -> None:
        """
        Преобразует каждую строчку с инструкцией в 4 байта.
        :return: None
        """
        for line in self.code_lines:
            parts = re.split(r', |,\t| |\t', line)
            parts[0] = parts[0].lower()

            if parts[0].endswith(':'):  # метка
                continue

            instruction = bytearray(4)
            instruction[0] = self.commands_dict[parts[0]]
            if parts[0] in self.vars_commands:  # работаем с переменными
                if len(parts) > 2:
                    instruction[1] = self.variables[parts[1]]
                    instruction[2:] = self.variables[parts[2]].to_bytes(2,
                                                                        'big')
                elif len(parts) == 2:
                    instruction[3] = self.variables[parts[1]]
            elif parts[0] in self.labels_commands:  # работаем с метками
                if len(parts) < 2:
                    raise Exception(f'Некорректная инструкция: "{line}"')
                instruction[2:] = self.labels[parts[1]].to_bytes(2, 'big')

            self.byte_code.extend(instruction)

    def get_byte_code(self, input_filename: str, output_filename: str) -> None:
        """
        Преобразует ассемблерный код в байт-код.
        :param input_filename: имя входного файла с ассемблерным кодом
        :param output_filename: имя выходного файла с байт-кодом
        :return: None
        """
        with open(input_filename, 'r', encoding='utf-8') as code:
            self.code_lines = filter(lambda x: x.strip(), code.readlines())
            self.code_lines = list(map(lambda x: x.strip(), self.code_lines))

        self.process_variables()
        self.process_labels()
        self.process_instructions()

        with open(output_filename, 'wb') as code:
            code.write(self.byte_code)
