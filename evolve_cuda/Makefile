CC = gcc
CXX = g++
NVC = nvcc

LDLIBS = -lglfw -lGLEW -lGL

all: libevolve.so

libevolve.so: evolve.cu
	nvcc $^ -o $@ --shared --compiler-options -fPIC

clean:
	rm -rf *.o *.so