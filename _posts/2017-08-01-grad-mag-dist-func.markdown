---
layout: post
title: Distance function has gradient magnitude equal to one
area: notes
tags:
- math
- level-sets
mathjax: true
comments: true
---

Suppose $\Omega$ is a subset of $\mathbb{R}^n$ with smooth boundary, $\partial\Omega$. Let's define the function,

$$
    g(x) = \min_{y \in \partial\Omega}|x-y|
$$

which gives the distance from a point to the boundary of the region.

Let's assume that the gradient of $g(x)$ is defined almost everywhere and show that it has magnitude one. This will also apply to the [signed distance function](https://en.wikipedia.org/wiki/Signed_distance_function) which is positive inside $\Omega$ and negative outside (or the opposite, depending on convention). The signed distance function is used in the [level set method](https://en.wikipedia.org/wiki/Level-set_method) and the PDE, $\|Dg\|=1$, is an instance of the [eikonal equation](https://en.wikipedia.org/wiki/Eikonal_equation).

First let's choose some $x$ and suppose that $y^* = \text{arg}\min_{y \in \partial\Omega} \|x-y\|$ is unique.

Now let's consider the line segment, $(1-t)x + ty^*$. Along this segment,

$$
\begin{align*}
|(1-t)x + ty - y^*| = |(1-t)x +ty - ty^* - (1-t)y^*)| &\leq (1-t)|x-y| + t|y-y^*| \\
\min_{y \in \partial\Omega} |(1-t)x + ty^*| &\leq \min_{y \in \partial\Omega} \biggl[ (1-t)|x-y| + t|y-y^*| \biggr] \\
g\left( (1-t)x + ty^*\right) &\leq (1-t)g(x) \\
\end{align*}
$$

but on the other hand, the inequality,

$$
    |(1-t)x + ty^* - y| = |x-y - t(x-y^*)| \geq |x-y| - t|x-y^*|
$$

yields the result,
$$
    g\left( (1-t)x + ty^*\right) \geq (1-t)g(x)
$$

So, we have that $g\left( (1-t)x + ty^*\right) = (1-t)g(x)$ where by taking derivatives with respect to $t$, we obtain the relation,

$$
    \langle Dg\left( (1-t)x + ty^*\right), y^*-x \rangle = -g(x)
$$

which says that
$$
    |Dg\left( (1-t)x + ty^*\right)| |y^*-x| \cos\theta = -g(x)
$$

... or since $\|y^* - x\| = g(x)$,

$$
    |Dg\left( (1-t)x + ty^*\right)| \cos\theta = -1
$$

Now note that when $t=0$, $Dg(x)$, points in the direction of maximal increase while $$y^*-x$$ points from $x$ to the closest point on the boundary, $$\partial\Omega$$. However, the direction, $$y^* - x$$, is clearly in the direction of maximum decrease since otherwise, $$y^*$$ would not be the minimizing point on the boundary. Therefore, $y^*-x = -Dg(x)$, so $\cos\theta = -1$, which must therefore hold for all $t \in [0,1]$.


So, we've shown that for any point, $x$, not on the boundary, if there is a unique closest point to the boundary, then we have,

$$
    |Dg| = 1
$$
