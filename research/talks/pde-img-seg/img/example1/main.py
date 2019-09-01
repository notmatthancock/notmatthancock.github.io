import numpy as np
from scipy.misc import imread
import matplotlib.pyplot as plt 
from scipy.ndimage import gaussian_gradient_magnitude as GGM

plt.xkcd()

img = imread('../one-circle.png').astype(np.float)[:,:,0]
img = (img - img.min()) / (img.max() - img.min())

s, ds = np.linspace(0, 2*np.pi, 100, retstep=True)

x = np.c_[np.cos(s), np.sin(s)]
x *= 90
x += 350

dt = 1.
stop_time = 200
sigma = 20
gmag = GGM(img, sigma)
damping = 5
V = np.exp(-damping*gmag)
V = (V-V.min()) / (V.max()-V.min())

i = 0
show_freq = 10


fig = plt.figure(figsize=(5, 5))
ax = fig.add_axes([0, 0, 1, 1])

def showsave(pause=False, save=True, show=False):
    print i
    ax.imshow(img, cmap=plt.cm.gray)
    ax.axis('off')
    lines, = ax.plot(x[:,0], x[:,1], '-r', label="t = {:.2f}".format(i*dt))
    ax.set_title("t = {:.2f}".format(i*dt))
    ax.legend(loc=1)
    if save:
        fig.savefig("{}.png".format(i))
    if pause:
        plt.pause(0.1)
    if show:
        plt.show()
    ax.cla()

showsave()
i += 1

while i*dt < stop_time:
    xs = np.vstack([x[-1], x, x[0]])
    xs = np.gradient(xs, ds, axis=0)[1:-1]
    nm = np.linalg.norm(xs, axis=1)
    xs /= nm[:,np.newaxis]
    N = np.c_[xs[:,1], -xs[:,0]]

    xint = x.round().astype(int)
    xint[xint < 0] = 0
    xint[:,0][xint[:,0] >= img.shape[0]-1] = img.shape[0]-1
    xint[:,1][xint[:,1] >= img.shape[1]-1] = img.shape[1]-1

    x += dt*N*V[xint[:,1], xint[:,0]][:,np.newaxis]
    x[x < 0] = 0
    x[:,0][x[:,0] >= img.shape[0]-1] = img.shape[0]-1
    x[:,1][x[:,1] >= img.shape[1]-1] = img.shape[1]-1

    if i % show_freq != 0:
        i += 1
        continue

    showsave()
    i += 1

showsave(pause=False, show=True)
