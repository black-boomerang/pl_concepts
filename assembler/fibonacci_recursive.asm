start:
    PRINT_STR "Введите число:"
    SCAN_INT cx
    PUSH cx
    CALL fib
    POP cx
    PRINT_INT ax
    STOP
fib:
    STACK_MOV bx, 4
    CMP bx, 1
    JG rec
    MOV ax, bx
    RET
rec:
    SUB bx, 1
    PUSH bx
    CALL fib
    POP bx
    MOV cx, ax
    SUB bx, 1
    PUSH cx
    PUSH bx
    CALL fib
    POP bx
    POP cx
    ADD ax, cx
    RET
