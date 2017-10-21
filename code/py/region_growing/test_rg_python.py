import numpy as np
import time
import region_growing_python as rgp
#from mayavi import mlab

nx = 61; ny = 51; nz = 71;

tx = np.linspace(-3,3,nx)
ty = np.linspace(-3,3,ny)
tz = np.linspace(-3,3,nz)

x,y,z = np.meshgrid(tx,ty,tz)

w = x**4 - 5*x**2 + y**4 - 5*y**2 + z**4 - 5*z**2

vol = -np.ones_like(w)
vol[np.logical_and(w >= 5, w<=20)] = 1.
vol[w <= -11] = 1.

seed = (11,45,35) # inner
#seed = (45,38,35) # outer
rgp.grow(vol, seed, 5)

start = time.time()
seg = rgp.grow(vol, seed, 5)
stop = time.time()

print("Ellapsed time: %.3f seconds." % (stop - start))
print("Errors: %d" % np.logical_xor(w <= -11, seg).sum())

#src = mlab.pipeline.scalar_field(seg.astype(np.float))
#mlab.pipeline.iso_surface(src, contours=[0.5], opacity=0.5)
#mlab.show()
