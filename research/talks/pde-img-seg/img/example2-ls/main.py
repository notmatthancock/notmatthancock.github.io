import numpy as np
from scipy.misc import imread
import matplotlib.pyplot as plt 
from scipy.ndimage import gaussian_gradient_magnitude as GGM
from scipy.ndimage import gaussian_filter as GF
from skimage.measure import find_contours
from slls.utils.masked_grad import gmag_os

plt.xkcd()

img = imread('../two-circle.png').astype(np.float)[:,:,0]
img = (img - img.min()) / (img.max() - img.min())

s, ds = np.linspace(0, 2*np.pi, 100, retstep=True)

x = np.c_[np.cos(s), np.sin(s)]
x *= 90
x += 250

ii, jj = np.indices(img.shape, dtype=np.float)
u = 90 - np.sqrt((ii-250)**2 + (jj-250)**2)
u = (u > 0).astype(np.float)*2 - 1

dt = 1.
stop_time = 250
sigma = 20
gmag = GGM(img, sigma)
damping = 5
V = np.exp(-damping*gmag)
V = (V-V.min()) / (V.max()-V.min())
G = GF(img, 5)
V *= (G.mean() - G)

fig = plt.figure(figsize=(5, 5))
ax = fig.add_axes([0, 0, 1, 1])
ax.axis('off')
ax.imshow(img, cmap=plt.cm.gray)

for i in range(1500+1):

    gmag = gmag_os(u, V)
    u += dt*V*gmag
    
    if i%100 != 0:
        continue

    print(i)
    lines = []
    for icontour, contour in enumerate(find_contours(u, 0)):
        if icontour == 0:
            kwargs = {'label': "t = {:.2f}".format(i*dt)}
        else:
            kwargs = {}
        lines.append(ax.plot(contour[:,1], contour[:,0], '-r', **kwargs)[0])

    ax.legend(loc=1)
    plt.pause(0.1)
    fig.savefig("{:d}.png".format(i))

    for line in lines:
        line.remove()
