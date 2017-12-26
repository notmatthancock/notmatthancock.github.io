---
layout: post
title: Equal area sphere partitioning
area: notes
tags:
- math
- python
mathjax: true
---

In this post, I'll discuss how to partition a sphere so that the resulting partitions have equal area. There are of course only five ways to do this if you require that the resulting patches are of identically shaped, corresponding to the five [Platonic solids](https://en.wikipedia.org/wiki/Platonic_solid). I'll discuss a different partitioning strategy that allows for more points. Thus, the partitions will not result in regular faces like the Platonic solid cases (i.e., identically shaped); however, the faces will be required to have equal area -- or rather, the surface area patches of the sphere that are enclosed by the sets of vertices corresponding to the partition of the sphere will have equal area.

Using [spherical coordinates](https://en.wikipedia.org/wiki/Spherical_coordinate_system), we can write, for a given radius, $r$, a sphere of radius $r$ as the set of points of the form

$$
    F(\theta, \phi) = \begin{bmatrix} r\cos(\theta)\sin(\phi) \\ r\sin(\theta)\sin(\phi) \\ r\cos(\phi) \end{bmatrix}
$$

where $0 \leq \theta \lt 2\pi$ and $0 \leq \phi \leq \pi$.

An immediate (and incorrect) way to proceed is to take samples $F(i \Delta\theta, j \Delta\phi)$ with $\Delta\theta = \frac{2\pi}{m}$, $\Delta\phi = \frac{\pi}{n}$, and $i,j$ running from zero to $m$ and $n$ respectively. Each rectangle in the $\theta,\phi$ plane has area $\Delta\theta\cdot\Delta\phi$, but on the sphere the areas are warped. Consider some sampled point in the $\theta,\phi$ plane, $(\theta_i, \phi_j)$ where $\theta_i = i\Delta\theta$ and $\phi_j = j\Delta\phi$. Then the corresponding surface area on the sphere is

$$
\begin{align*}
    \Delta S
    &= \int_{\theta_i}^{\theta_{i+1}} \int_{\phi_j}^{\phi_{j+1}} r^2 \sin(\phi) \; d\phi d\theta \\
    &= r^2 \Delta\theta \bigl( \cos(\phi_{j}) - \cos(\phi_{j+1}) \bigr)
\end{align*}
$$

This says that the surface area on the sphere changes depending on $\phi$ when we sample on a uniform rectangular grid in $\theta$ and $\phi$. The area becomes smaller near the "north and south poles" of the sphere. We can illustrate this with some Python code:

{% highlight python %}
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

r = 1.0

t = np.linspace(0, 2*np.pi, 20)
p = np.linspace(0,   np.pi, 10)

theta,phi = np.meshgrid(t,p)

x = r*np.cos(theta)*np.sin(phi)
y = r*np.sin(theta)*np.sin(phi)
z = r*np.cos(phi)

fig = plt.figure(figsize=(10,4))
ax1 = fig.add_subplot(121)
ax2 = fig.add_subplot(122, projection='3d')

ax1.plot(theta.flatten(), phi.flatten(), 'o')
ax1.set_xlabel("$\\theta$")
ax1.set_ylabel("$\\phi$")

ax2.plot_surface(x,y,z, edgecolors='0.2')

plt.show()
{% endhighlight %}

which yields

<img style="border: 1px solid #333" src="{{ site.baseurl }}/images/sphere-sample-uniform-theta-phi.svg">

<br>

Let's now instead use the formula for the surface area $\Delta S$ to obtain a correct sampling. Let's suppose $\Delta S$ and $\Delta \theta$ have been fixed a priori, and let's suppose we begin with some initial $\phi_0$. Note by fixing $\Delta S$, we are solving the problem of obtaining an equal-surface-area partition directly.

The formula above for $\Delta S$ indicates a recursion for $\phi_j$, $j=1,2,\ldots$, i.e.,

$$
    \phi_{j+1} = \cos^{-1}\left( \cos(\phi_j) - \frac{\Delta S}{r^2 \Delta\theta} \right)
$$

A closed form is simple to derive by denoting $c_j = \cos(\phi_j)$ and observing $c_{j+1} = c_0 - j\frac{\Delta S}{r^2 \Delta\theta}$ and thus,

$$
    \phi_{j+1} = \cos^{-1}\left( \cos(\phi_0) - j \frac{\Delta S}{r^2 \Delta\theta} \right)
$$

Let's make the simplifying assumption that $\phi_0 = 0$ and note that the argument to $\cos^{-1}$ is decreasing and thus valid when the argument is greater than or equal to negative one, i.e.,

$$
    1-j\frac{\Delta S}{r^2 \Delta\theta} \geq -1 \;\; \Rightarrow \;\;  j \leq \frac{2 r^2 \Delta\theta}{\Delta S}
$$

If we make the simplifying assumption that $r$ is an integer and $\Delta S = \frac{\Delta\theta}{n}$, then $j$ achieves its upper bound at $j = 2r^2n$. We can augment the above script a tad to visualize the equal area partition:

{% highlight python %}
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

n = 10
r = 1.0

t,delta_theta = np.linspace(0, 2*np.pi, 10, retstep=True)
delta_S = delta_theta / n

p = 1-np.arange(2*n+1) * delta_S / (r**2 * delta_theta) 
p = np.arccos(p)

theta,phi = np.meshgrid(t,p)

x = r*np.cos(theta)*np.sin(phi)
y = r*np.sin(theta)*np.sin(phi)
z = r*np.cos(phi)

fig = plt.figure(figsize=(10,4))
ax1 = fig.add_subplot(121)
ax2 = fig.add_subplot(122, projection='3d')

ax1.plot(theta.flatten(), phi.flatten(), 'o')
ax1.set_xlabel("$\\theta$")
ax1.set_ylabel("$\\phi$")

ax2.plot_surface(x,y,z, edgecolors='0.2')

plt.show()
{% endhighlight %}

<img style="border: 1px solid #333" src="{{ site.baseurl }}/images/sphere-sample-equal.svg">

Note that the rectangles closer to the equator are shorter and wider to maintain equal area by accounting for the fact that when $\phi$ is close to $\pi/2$, increments in $\Delta\theta$ produce a longer longitudinal step.
