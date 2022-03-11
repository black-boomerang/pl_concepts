start:
    PRINT_STR "Введите число"
    SCAN_INT cx
    MOV ax, 0
    MOV bx, 1
loop_start:
    CMP cx, 0
    JE loop_end
    MOV dx, ax
    ADD ax, bx
    MOV bx, dx
    SUB cx, 1
    JMP loop_start
loop_end:
    PRINT_INT ax
    STOP
