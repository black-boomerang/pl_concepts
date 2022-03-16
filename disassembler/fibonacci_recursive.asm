start:
	print_str "Введите число:"
	scan_int var_3
	push var_3
	call label_1
	pop var_3
	print_int var_1
	stop
label_1:
	stack_mov var_2, 4
	cmp var_2, 1
	jg label_2
	mov var_1, var_2
	ret
label_2:
	sub var_2, 1
	push var_2
	call label_1
	pop var_2
	mov var_3, var_1
	sub var_2, 1
	push var_3
	push var_2
	call label_1
	pop var_2
	pop var_3
	add var_1, var_3
	ret