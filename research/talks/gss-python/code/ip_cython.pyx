import numpy as np
cimport numpy as np
cimport cython

DTYPE = np.float64
ctypedef np.float64_t dtype_t

@cython.boundscheck(False)
def inner_product(np.ndarray[dtype_t, ndim=1] x,
                  np.ndarray[dtype_t, ndim=1] y):
    cdef float z = 0.0
    cdef int n = x.shape[0]
    cdef int i
    for i in range(n):
        z += x[i]*y[i]
    return z
