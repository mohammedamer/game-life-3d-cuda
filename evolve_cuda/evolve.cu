#include <iostream>
#include <math.h>

struct index {
  int x;
  int y;
  int z;
};

__device__
struct index unravel_idx(int idx, int n){

  struct index unravel;

  int x, y, z;

  z = idx % n;
  y = (idx / n) % n;
  x = (idx / n) / n;

  unravel = {.x = x, .y = y, .z = z};

  return unravel;

} 

__device__
int ravel_idx(struct index idx, int n){
  return idx.x*n*n+idx.y*n + idx.z;
}

__device__
int should_live(int is_alive, int alive_count){

  if (is_alive == 1){

    if (alive_count < 4 || alive_count > 5){
      return 0;
    }

  } else{

    if (alive_count == 5){
      return 1;
    }

  }

  return is_alive;

}

__global__
void evolve_kernel(int *cell_arr, int *out_arr, int n)
{
  int num_elem = n*n*n;

  // cell index
  int current_idx = blockIdx.x*blockDim.x+threadIdx.x;

  // grid-stride loop

  for (int idx=current_idx;
    idx<num_elem; 
    idx+=blockDim.x*gridDim.x){

      struct index idx_3d = unravel_idx(idx, n);

      int alive_count = 0;

      // collect adjacent

      int adj_x[] = {idx_3d.x-1, idx_3d.x, idx_3d.x+1};

      int adj_y[] = {idx_3d.y-1, idx_3d.y, idx_3d.y+1};

      int adj_z[] = {idx_3d.z-1, idx_3d.z, idx_3d.z+1};

      // count live

      for (int i = 0; i < 3; i++){
        for (int j = 0; j < 3; j++){
          for (int k=0; k<3; k++){

            struct index _idx;

            _idx.x = adj_x[i];
            _idx.y = adj_y[j];
            _idx.z = adj_z[k];

            if ((_idx.x > -1 && _idx.x < n) &&
            (_idx.y > -1 && _idx.y < n) &&
            (_idx.z > -1 && _idx.z < n)){
              
              int adj_idx = ravel_idx(_idx, n);

              if (adj_idx != idx){
                alive_count+=cell_arr[adj_idx];
              } 
            }

          }
        }
      }

      int is_alive = cell_arr[current_idx];

      // apply local rules

      out_arr[current_idx] = should_live(is_alive, alive_count);

    }

}

void evolve(int *cell_arr, int *out_arr, int n)
{
  
  int *_in, *_out;
  int num_elem;

  num_elem = n*n*n;

  // allocate unified mem

  cudaMallocManaged(&_in, num_elem*sizeof(int));
  cudaMallocManaged(&_out, num_elem*sizeof(int));

  // copy input

  for (int i = 0; i < num_elem; i++) {
    _in[i] = cell_arr[i];
  }

  // call kernel

  int threadsPerBlock = 256;
  int blocks = (num_elem+threadsPerBlock)/threadsPerBlock;

  evolve_kernel<<<blocks,threadsPerBlock>>>(_in, _out, n);

  // sync with GPU

  cudaDeviceSynchronize();

  cudaFree(_in);

  // copy output

  for (int i = 0; i < num_elem; i++) {
    out_arr[i] = _out[i];
  }

  cudaFree(_out);
}