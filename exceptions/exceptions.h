#pragma once
#include <csetjmp>
#include <exception>
#include <stack>
#include <iostream>

class BaseException : public std::exception {
public:
    const char* what() const throw();
};

class DerivedException : public BaseException {
public:
    const char* what() const throw();
};

class OtherException : public std::exception {
public:
    const char* what() const throw();
};

// базовый класс объекта, от которого необходимо наследовать все остальные объекты,
// (необходимо для вызова деструкторов при исключениях)
class Object {
public:
    static std::stack<Object*> objects;

    Object() {
        objects.push(this);
    }

    virtual ~Object() {
        objects.pop();
    }
};

// элемент списка с контекстом
struct JmpList {
    JmpList* prev;
    size_t objects_count; // количество созданных объектов на момент вызова try
    jmp_buf env;

    JmpList(JmpList* prev, size_t objects_count) :
        prev(prev), objects_count(objects_count) {}
};
