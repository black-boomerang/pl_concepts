### Команды для ассемблера:
+ print (0x01) - напечатать строку;
+ print_int (0x02) - напечатать число;
+ scan_int (0x03) - считать число;
+ mov (0x04) - поместить значение из переменной источника в переменную приёмника;
+ add (0x05) - прибавить значение из переменной источника к переменной приёмника;
+ sub (0x06) - отнять значение из переменной источника от переменной приёмника;
+ cmp (0x07) - сравнить значения переменной источника и переменной приёмника;
+ je (0x08) - если выполнено равенство, переместиться по метке;
+ jmp (0x09) - переместиться по метке;
+ jg (0x0A) - если выполнено неравенство "больше", переместиться по метке;
+ call (0x0B) - вызвать функцию;
+ ret (0x0C) - возврат из функции;
+ push (0x0D) - положить значение на стек;
+ pop (0x0E) - снять значение со стека;
+ stack_mov (0x0F) - поместить в переменную приёмника значение из стека (по смещению относительно ESP);
+ stop (0xFF) - прекратить выполнение программы.