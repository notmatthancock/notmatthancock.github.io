import numpy as np
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

src = mlab.pipeline.scalar_field(w)

mlab.pipeline.iso_surface(src, contours=[5,20], opacity=0.5)
mlab.pipeline.iso_surface(src, contours=[-11], opacity=0.5)
mlab.savefig('tangle-cube-inner-and-outer.png')
