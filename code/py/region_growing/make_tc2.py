import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as manim

nx = 61; ny = 51; nz = 71;

tx = np.linspace(-3,3,nx)
ty = np.linspace(-3,3,ny)
tz = np.linspace(-3,3,nz)

x,y,z = np.meshgrid(tx,ty,tz)

w = x**4 - 5*x**2 + y**4 - 5*y**2 + z**4 - 5*z**2

vol = -np.ones_like(w)
vol[np.logical_and(w >= 5, w<=20)] = 1.
vol[w <= -11] = 1.

fig = plt.figure(figsize=(3,3))
ax  = fig.add_subplot(111)
img = ax.imshow(vol[:,:,0], vmin=-1, vmax=1,
                cmap=plt.cm.gray, interpolation='bilinear')

writer = manim.ImageMagickWriter(fps=3)
with writer.saving(fig, 'tangle-cube.gif', 100):
    for i in range(nz):
        print(i)
        img.set_data(vol[:,:,i])
        ax.set_title("%02d" % i)
        writer.grab_frame()
