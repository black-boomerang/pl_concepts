start:
	print_str "Вычисление n-го числа Фибоначчи."
	print_str "Введите число:"
	scan_int var_4
	mov var_1, 0
	mov var_3, 1
label_1:
	cmp var_4, 0
	je label_2
	mov var_2, var_1
	add var_1, var_3
	mov var_3, var_2
	sub var_4, 1
	jmp label_1
label_2:
	print_int var_1
	stop