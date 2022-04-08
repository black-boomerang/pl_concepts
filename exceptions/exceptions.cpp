#include "exceptions.h"

const char* BaseException::what() const throw() {
    return "Catched base exception\n";
}

const char* DerivedException::what() const throw() {
    return "Catched derived exception\n";
}

const char* OtherException::what() const throw() {
    return "Catched other exception\n";
}

