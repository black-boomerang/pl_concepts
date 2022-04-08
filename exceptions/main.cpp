#include <csetjmp>
#include <iostream>
#include "exceptions.h"

// определяем пользовательский объект
class CustomObject : public Object {
public:
    static int objects_count;
    int num;

    CustomObject() {
        num = ++objects_count;
        std::cout << "Custom object " << num << " created\n";
    }

    ~CustomObject() {
        std::cout << "Custom object " << num << " destroyed\n";
    }
};

JmpList* current_jmp = nullptr;
std::exception* thrown_exception;
int CustomObject::objects_count = 0;
std::stack<Object*> Object::objects;

// определяем макросы try/catch/throw/finally, а также вспомогательные
// _change_env и _clear_stack
#define _change_env \
prev_jmp = current_jmp->prev; \
delete current_jmp; \
current_jmp = prev_jmp; \

#define _clear_stack \
for (size_t i = Object::objects.size(); i > current_jmp->objects_count; --i) { \
    Object::objects.top()->~Object(); \
} \

#define try { \
JmpList* prev_jmp = current_jmp; \
current_jmp = new JmpList(prev_jmp, Object::objects.size()); \
if (setjmp(current_jmp->env) == 0) {

#define catch(type, exception) \
} else if (auto* casted_exception = dynamic_cast<type*>(thrown_exception)) { \
    type exception = *casted_exception;

#define throw(exception) \
if (thrown_exception) { \
    std::terminate(); \
} \
thrown_exception = new decltype(exception)(exception); \
_clear_stack \
longjmp(current_jmp->env, 1);

#define finally \
} else { \
    if (!current_jmp->prev) { \
        std::terminate(); \
    } \
    _change_env \
    _clear_stack \
    longjmp(current_jmp->env, 1); \
} \
_change_env \
delete thrown_exception; \
thrown_exception = nullptr; \
}

void function1() {
    std::cout << "Function 1 started\n";
    try {
        CustomObject obj;
        BaseException base_exception;
        throw(base_exception);
    } catch (DerivedException, e) {
        std::cout << e.what();
    }
    finally
}

void function2() {
    std::cout << "Function 2 started\n";
    try {
        CustomObject obj;
        function1();
    } catch (BaseException, e) {
        std::cout << e.what();
    }
    finally
}

void function3() {
    std::cout << "Function 3 started\n";
    try {
        CustomObject obj;
        OtherException other_exception;
        throw(other_exception);
    }
    catch (DerivedException, e) {
        std::cout << e.what();
    }
    finally
}

void function4() {
    std::cout << "Function 4 started\n";
    try {
        CustomObject obj;
        function3();
    }
    catch (OtherException, e) {
        std::cout << e.what();
    }
    finally
}

void function5() {
    std::cout << "Function 5 started\n";
    try {
        CustomObject obj;
        function4();
    }
    catch (OtherException, e) {
        std::cout << e.what();
    }
    finally
}

int main() {
    std::cout << "Call 1:\n";
    function2(); // бросается базовая ошибка, которая ловится во втором catch
    std::cout << "\nCall 2:\n";
    function5(); // бросается другая ошибка, которая ловится во втором catch
}
