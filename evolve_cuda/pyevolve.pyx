# distutils: language=c++

cdef extern from "evolve.h":
    void evolve(int *cell_arr, int *out_arr, int n)

def pyevolve(int[::1] cell_arr, int[::1] out_arr, int n):
    evolve(&cell_arr[0], &out_arr[0], n)