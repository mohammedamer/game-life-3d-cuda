import numpy as np
import pyevolve


n = np.int32(10)
in_arr = np.zeros(shape=(n,n,n), dtype=np.int32).reshape(-1)
out_arr = np.empty_like(in_arr).reshape(-1)

pyevolve.pyevolve(in_arr, out_arr, n)

print(out_arr)