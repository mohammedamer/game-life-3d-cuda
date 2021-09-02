import itertools
import argparse

import numpy as np

from ursina import Ursina
from ursina import Entity
from ursina import camera
from ursina import window
from ursina.lights import DirectionalLight
from ursina import time

from utils import iterate_cubes
from utils import get_cubes_alive_arr
from utils import update_cubes_alive_arr
from utils import Cube

import pyevolve

parser = argparse.ArgumentParser()
parser.add_argument('-c', type=int, default=10, help='number of cubes per dim')

args = parser.parse_args()

if args.c < 1:
    raise ValueError('Invalid cubes number')

CUBES_PER_DIM = args.c


def init_cubes(cubes_per_dim):

    half_cubes_num = int(cubes_per_dim/2.)

    start_x = -(half_cubes_num)
    start_y, start_z = start_x, start_x

    if cubes_per_dim % 2 == 0:
        end_x, end_y, end_z = [-start_x]*3
    else:
        end_x, end_y, end_z = [-start_x+1]*3

    x_range = np.arange(start_x, end_x)
    y_range = np.arange(start_y, end_y)
    z_range = np.arange(start_z, end_z)

    cubes = []

    for x in x_range:

        y_row = []

        for y in y_range:

            z_row = []

            for z in z_range:

                cube = Cube(pos=(x+0.5, y+0.5, z+0.5))
                z_row.append(cube)

            y_row.append(z_row)

        cubes.append(y_row)

    return cubes, (start_x, start_y, start_z), (end_x, end_y, end_z)


def adjust_camera(start_vec, end_vec):

    camera_pos = end_vec[0]+20, end_vec[1]+20, start_vec[2]-20
    camera.position = camera_pos
    camera.look_at(target=(0, 0, 0))


def init_game(cubes_per_dim):

    cubes, start_vec, end_vec = init_cubes(cubes_per_dim)

    start_vec, end_vec = np.array(start_vec), np.array(end_vec)

    adjust_camera(start_vec, end_vec)

    pivot = Entity()
    DirectionalLight(
        parent=pivot, x=end_vec[0]+20, y=end_vec[1]+20, z=start_vec[2]-20, shadows=True)

    return cubes


def seed_cubes(cubes):

    for cube, _ in iterate_cubes(cubes):

        enabled = np.random.rand() < 0.2

        cube.enable() if enabled else cube.disable()


def evolve(cubes, cubes_per_dim):

    current_alive_arr = get_cubes_alive_arr(cubes).astype(np.int32).reshape(-1)
    new_alive_arr = np.empty_like(current_alive_arr)

    pyevolve.pyevolve(current_alive_arr, new_alive_arr,
                      np.int32(cubes_per_dim))

    new_alive_arr = new_alive_arr.reshape((cubes_per_dim,)*3)

    update_cubes_alive_arr(cubes, alive_arr=new_alive_arr)


delta_t = 0


def update():

    global delta_t

    if delta_t > 0.5:
        evolve(cubes, cubes_per_dim=CUBES_PER_DIM)
        delta_t = 0
    else:
        delta_t += time.dt


''' default values
    camera default position: (0,0,-20)
    camera default rotation: (0,0,0)
    camera default fov: 40
    entity default position (0,0,0)
'''

app = Ursina()

cubes = init_game(cubes_per_dim=CUBES_PER_DIM)
print('init completed')

seed_cubes(cubes)
print('seeding completed')

app.run()
