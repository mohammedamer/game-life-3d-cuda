import itertools

import numpy as np

from ursina import Entity
from ursina.shaders import lit_with_shadows_shader
from ursina import color


class Cube:

    def __init__(self, pos):
        self.entity = None
        self.pos = pos

    def enable(self):

        if self.entity == None:
            self.entity = Entity(model='cube', position=self.pos,
                                 color=color.orange, texture='white_cube', shader=lit_with_shadows_shader)

        self.entity.enabled = True

    def disable(self):

        if self.entity != None:
            self.entity.enabled = False

    def is_enabled(self):

        if self.entity != None:
            return self.entity.enabled

        return False

# python implemention of the same functionality in CUDA


def should_live(alive_count, is_alive):

    if is_alive:

        if alive_count < 4 or alive_count > 5:
            return False

    else:

        if alive_count == 5:
            return True

    return is_alive

# python implemention of the same functionality in CUDA


def evolve(cubes, cubes_per_dim):

    current_alive_arr = get_cubes_alive_arr(cubes)
    new_alive_arr = np.empty_like(current_alive_arr)

    for (i, j, k), is_alive in np.ndenumerate(current_alive_arr):

        adj_i = (i-1, i, i+1)
        adj_j = (j-1, j, j+1)
        adj_k = (k-1, k, k+1)

        alive_count = 0
        for _i, _j, _k in itertools.product(adj_i, adj_j, adj_k):

            if not (_i == i and _j == j and _k == k):

                boundary = False
                for coord in (_i, _j, _k):
                    if coord < 0 or coord > cubes_per_dim-1:
                        boundary = True

                if not boundary:

                    alive_count += current_alive_arr[_i][_j][_k]

        new_alive_arr[i, j, k] = 1 if should_live(
            alive_count=alive_count, is_alive=is_alive) else 0

    update_cubes_alive_arr(cubes, alive_arr=new_alive_arr)


def iterate_cubes(cubes):

    for i, y_row in enumerate(cubes):
        for j, z_row in enumerate(y_row):
            for k, cube in enumerate(z_row):
                yield cube, (i, j, k)


def get_cubes_alive_arr(cubes):

    alive_arr = []

    for i, y_row in enumerate(cubes):

        y_arr = []
        for j, z_row in enumerate(y_row):

            z_arr = []
            for k, cube in enumerate(z_row):
                z_arr.append(1 if cube.is_enabled() else 0)

            y_arr.append(z_arr)

        alive_arr.append(y_arr)

    return np.array(alive_arr)


def update_cubes_alive_arr(cubes, alive_arr):

    for cube, (i, j, k) in iterate_cubes(cubes):

        if alive_arr[i, j, k] == 1:
            cube.enable()
        else:
            cube.disable()
