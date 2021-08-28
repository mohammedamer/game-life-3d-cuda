import itertools

import numpy as np

from ursina import Ursina, texture
from ursina import color
from ursina import Entity
from ursina import camera
from ursina import window
from ursina.shaders import lit_with_shadows_shader
from ursina.lights import DirectionalLight
from ursina import time

import pyevolve

CUBES_PER_DIM = 10

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
                z_arr.append(1 if cube.visible else 0)

            y_arr.append(z_arr)

        alive_arr.append(y_arr)

    return np.array(alive_arr)

def update_cubes_alive_arr(cubes, alive_arr):

    for cube, (i, j, k) in iterate_cubes(cubes):
        cube.visible = alive_arr[i,j,k] == 1
        

def init_cubes(cubes_per_dim):

    half_cubes_num = int(cubes_per_dim/2.)

    start_x = -(half_cubes_num)
    start_y, start_z = start_x, start_x

    if cubes_per_dim%2 == 0:
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

                cube = Entity(model='cube', position=(x+0.5,y+0.5,z+0.5), 
                color=color.orange, texture='white_cube', shader=lit_with_shadows_shader)
                cube.visible = False
                z_row.append(cube)

            y_row.append(z_row)
        
        cubes.append(y_row)

    return cubes, (start_x, start_y, start_z), (end_x, end_y, end_z)

def adjust_camera(start_vec, end_vec):

    camera_pos = end_vec[0]+20, end_vec[1]+20, start_vec[2]-20
    camera.position = camera_pos
    camera.look_at(target=(0,0,0))


def init_game(cubes_per_dim):

    cubes, start_vec, end_vec = init_cubes(cubes_per_dim)
    
    start_vec, end_vec = np.array(start_vec), np.array(end_vec)

    adjust_camera(start_vec, end_vec)

    pivot = Entity()
    DirectionalLight(parent=pivot, x=end_vec[0]+20, y=end_vec[1]+20, z=start_vec[2]-20, shadows=True)

    return cubes

def seed_cubes(cubes):

    for cube, _ in iterate_cubes(cubes):

        visible = np.random.rand() < 0.2

        cube.visible = visible

# def should_live(alive_count, is_alive):

#     if is_alive:

#         if alive_count < 4 or alive_count > 5:
#             return False

#     else:

#         if alive_count == 5:
#             return True

#     return is_alive


# def evolve(cubes):

#     current_alive_arr = get_cubes_alive_arr(cubes)
#     new_alive_arr = np.empty_like(current_alive_arr)

#     for (i, j, k), is_alive in np.ndenumerate(current_alive_arr):

#         adj_i = (i-1, i, i+1)
#         adj_j = (j-1, j, j+1)
#         adj_k = (k-1, k, k+1)

#         alive_count = 0
#         for _i, _j, _k  in itertools.product(adj_i, adj_j, adj_k):

#             if not (_i == i and _j == j and _k == k):

#                 boundary = False
#                 for coord in (_i, _j, _k): 
#                     if coord < 0 or coord > CUBES_PER_DIM-1:
#                         boundary = True

#                 if not boundary:

#                     alive_count+=current_alive_arr[_i][_j][_k]

#         new_alive_arr[i,j,k] = 1 if should_live(alive_count=alive_count, is_alive=is_alive) else 0

#     update_cubes_alive_arr(cubes, alive_arr=new_alive_arr)

def evolve(cubes):

    current_alive_arr = get_cubes_alive_arr(cubes).astype(np.int32).reshape(-1)
    new_alive_arr = np.empty_like(current_alive_arr)

    pyevolve.pyevolve(current_alive_arr, new_alive_arr, np.int32(CUBES_PER_DIM))

    new_alive_arr = new_alive_arr.reshape((CUBES_PER_DIM,)*3)

    update_cubes_alive_arr(cubes, alive_arr=new_alive_arr)

delta_t = 0

def update():

    global delta_t

    if delta_t > 0.5:    
        evolve(cubes)
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
seed_cubes(cubes)

app.run()