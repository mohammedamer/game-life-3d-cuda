// #include <iostream>
// #include <math.h>

int get_number(float num)
{
  return num*5;
}

// // function to add the elements of two arrays
// __global__
// void evolve_kernel(int n, float *x, float *y)
// {
//   for (int i = 0; i < n; i++)
//       y[i] = x[i] + y[i];
// }

// void evolve(int n, float *x, float *y)
// {
  
//   float *_x, *_y;

//   cudaMallocManaged(&x, n*sizeof(float));
//   cudaMallocManaged(&y, n*sizeof(float));

//   // initialize x and y arrays on the host
//   for (int i = 0; i < N; i++) {
//     x[i] = 1.0f;
//     y[i] = 2.0f;
//   }

//   evolve_kernel<<<1,1>>>(N, x, y);

//   cudaDeviceSynchronize();

//   // Check for errors (all values should be 3.0f)
//   float maxError = 0.0f;
//   for (int i = 0; i < N; i++)
//     maxError = fmax(maxError, fabs(y[i]-3.0f));
//   std::cout << "Max error: " << maxError << std::endl;

//   // Free memory
//   cudaFree(x);
//   cudaFree(y);

//   return 0;
// }