# distutils: language=c++

cdef extern from "./evolve.h":
    int get_number(float num)

def pyget_number(num):
    return get_number(num)