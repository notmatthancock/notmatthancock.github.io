import numpy as np
import time
import region_growing_python as rgp
import region_growing as rgc
from mayavi import mlab

nx = 61; ny = 51; nz = 71;

tx = np.linspace(-3,3,nx)
ty = np.linspace(-3,3,ny)
tz = np.linspace(-3,3,nz)

x,y,z = np.meshgrid(tx,ty,tz)

w = x**4 - 5*x**2 + y**4 - 5*y**2 + z**4 - 5*z**2

vol = -np.ones_like(w)
vol[np.logical_and(w >= 5, w<=20)] = 1.
vol[w <= -11] = 1.

#vol += np.random.randn(*vol.shape)*0.05

seed = (11,45,35) # inner
#seed = (45,38,35) # outer

start = time.time()
segpy = rgp.grow(vol, seed, 5)
stop = time.time()

print("(Python) Ellapsed time: %.3f seconds." % (stop - start))
print("(Python) Errors: %d" % np.logical_xor(w <= -11, segpy).sum())

start = time.time()
segc = rgc.grow(vol, seed[0], seed[1], seed[2], 5) 
stop = time.time()

print("(C)      Ellapsed time: %.3f seconds." % (stop - start))
print("(C)      Errors: %d" % np.logical_xor(w <= -11, segc).sum())
