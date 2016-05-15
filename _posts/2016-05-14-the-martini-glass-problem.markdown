---
layout: post
title: The martini glass problem
tags: math 
mathjax: true
---

This problem comes from [a riddle at the five thirty-eight](http://fivethirtyeight.com/features/can-you-solve-the-puzzle-of-the-overflowing-martini-glass/). Basically, the problem is this:

*You have a conical martini glass, which is filled such that the length of the liquid up the side of the glass is ratio, $p$, of the total length of the side of the glass. When the glass is tipped so that the liquid just reaches the brim, what distance does the liquid go up the opposite side of the glass?*

Here's two approaches, and an applet to play with:

## Plane geometry solution 

<a href="javascript:show_geo_solution();" id="geo-solution-link">Show solution</a>
<script>
    function show_geo_solution() {
        var s = document.getElementById('geo-solution');
        var l = document.getElementById('geo-solution-link');
        if (s.style.display == 'none') {
            s.style.display = 'block';
            l.innerHTML = 'Hide solution';
        }
        else {
            s.style.display = 'none';
            l.innerHTML = 'Show solution';
        }
    }
</script>

<div id="geo-solution" style="display:none">
    First, the problem is simplified by the symmetry of glass. When looked upon parallel to the table on which the glass sits, the glass is a triangle, and the liquid contained within the glass forms a similar triangle, sharing an angle with the base-angle of the glass.<br>
    <br>
    Suppose the distance of the side of the glass is $D$, and the distance of the liquid up the side of the glass when the glass is level is $d = pD$. Suppose angle of the base of the glass is $\theta$. You can view these quantities below in the applet. So using the "side-angle-side" formula, the area occupied by the liquid in the triangle is:

    $$
        A = \frac{1}{2}d^2\sin(\theta)
    $$

    This area is conserved when the glass is tilted. Suppose (without loss of generality) that the glass is tilted to the right. In this case, the distance up the side of the glass on the right is larger than the left. Denote these distances $d_R$ and $d_L$, respectively. Now, the area is:

    $$
        A = \frac{1}{2}d_Ld_R\sin(\theta)
    $$

    Equating the two, we have that $d^2 = d_Ld_R$. So, when the liquid reaches the top of the glass (i.e., $d_R = D$), the distance on the opposite side is:

    $$
        d_L^* = \frac{d^2}{D} = p^2D
    $$
</div>

## Linear algebra solution

<a href="javascript:show_linalg_solution();" id="linalg-solution-link">Show solution</a>
<script>
    function show_linalg_solution() {
        var s = document.getElementById('linalg-solution');
        var l = document.getElementById('linalg-solution-link');
        if (s.style.display == 'none') {
            s.style.display = 'block';
            l.innerHTML = 'Hide solution';
        }
        else {
            s.style.display = 'none';
            l.innerHTML = 'Show solution';
        }
    }
</script>

<div id="linalg-solution" style="display:none">

Let $\mathbf{D} = \begin{bmatrix} x_L \\ y_L\end{bmatrix}$ denote the position vector of the top right corner of the triangle representing the martini glass, such that this distance is $D = ||\mathbf{D}||$. The position vector of the liquid at the upper-most right side of the glass when the glass is level is $\mathbf{d}_R = p\mathbf{D}$. Similarly when the glass is level, the position vector for the top-left part of the liquid is $\mathbf{d}_L = p\begin{bmatrix} -x_L \\ y_L \end{bmatrix}$. The area occupied by the liquid when the glass is level is then:

$$
    A = \frac{1}{2} \text{det}\left( \begin{bmatrix} \mathbf{d}_L \; \mathbf{d}_R \end{bmatrix} \right) = p^2 \cdot x_L \cdot y_L
$$

When the glass is tipped, this is equivalent to scaling the vector, $\mathbf{d}_R$ by some factor, $t \in [1,\frac{1}{p}]$, since $\frac{1}{p}\mathbf{d}_R = \mathbf{D}$. As $t$ goes from $1$ to $\frac{1}{p}$, the vector, $\mathbf{d}_L$ is also scaled, but not by some unknown factor, say $c(t)$, which depends on $t$. We again use the area conservation of the liquid to determine $c(t)$:

$$
    A = \frac{1}{2} \text{det}\left( \begin{bmatrix} c(t)\mathbf{d}_L \; t\mathbf{d}_R \end{bmatrix} \right) = c(t) \cdot t \cdot p^2 \cdot x_L \cdot y_L
$$

Equating the two areas, we have that $c(t) = \frac{1}{t}$. Thus, we the liquid reach the brim (i.e., $t=\frac{1}{p}$), the distance of the liquid on the opposite side is $||c(t) \mathbf{d}_L|| = p^2D$, which agrees with the previous solution.

</div>

## Applet

<iframe scrolling="no" src="https://www.geogebra.org/material/iframe/id/rzvu62Rx/width/804/height/607/border/888888/rc/false/ai/false/sdz/true/smb/false/stb/false/stbh/true/ld/false/sri/true/at/auto" width="804px" height="607px" style="border:0px;"> </iframe>
