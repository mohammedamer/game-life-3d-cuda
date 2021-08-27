CC = gcc
CXX = g++
NVC = nvcc

LDLIBS = -lglfw -lGLEW -lGL

all: main

# game_life_3d: game_life_3d.cu
# nvcc $^ -o $@

# main: main.o

main: main.cpp


clean:
	rm -rf *.o