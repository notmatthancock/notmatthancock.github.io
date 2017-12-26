import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

t = np.linspace(0, 2*np.pi, 20)
p = np.linspace(0,   np.pi, 10)

theta,phi = np.meshgrid(t,p)

x = np.cos(theta)*np.sin(phi)
y = np.sin(theta)*np.sin(phi)
z = np.cos(phi)

fig = plt.figure(figsize=(10,4))
ax1 = fig.add_subplot(121)
ax2 = fig.add_subplot(122, projection='3d')

ax1.plot(theta.flatten(), phi.flatten(), 'o')
ax1.set_xlabel("$\\theta$")
ax1.set_ylabel("$\\phi$")

ax2.plot_surface(x,y,z, edgecolors='0.2')

plt.show()
