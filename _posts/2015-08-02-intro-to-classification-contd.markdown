---
layout: post
title: Intro to Classification (Numerical Example with Python)
tags: math pattern-recognition python
mathjax: true
published: false
---

This post is a continuation of the [previous introduction to binary classification]({{ site.baseurl }}/2015/07/24/intro-to-binary-classification.html). I'll go over some Python code to implement the logistic model discussed in the previous post. We'll use simple gradient ascent to find the model parameters.

### Sample data

Consider $p=2$, $P(Y=1)=0.6$, and $P(X\|Y=j) \sim \mathcal{N}(\mu_j, I)$ where $I$ is the identity matrix and $\mu_0 = \begin{bmatrix} -1 & -1 \end{bmatrix}^T$, $\mu_1 = \begin{bmatrix} 1 & 1 \end{bmatrix}^T$. We can generate some sample data with $n=200$ (realizations of the random variables $\mathbf{X}$ and $\mathbf{Y}$ mentioned in the previous post) using the following:

{% highlight python %}
import numpy as np

rs = np.random.RandomState(1234)
p = 0.6 
mean1 = np.r_[1,1.]
mean0 = -mean1

Y = (rs.rand(200) > p).astype(int)
X = np.zeros((200,2))
X[Y==0] = rs.multivariate_normal(mean0, np.eye(2), size=(Y==0).sum())
X[Y==1] = rs.multivariate_normal(mean1, np.eye(2), size=(Y==1).sum())
{% endhighlight %}

...and we can plot the data with:

{% highlight python %}
import matplotlib.pyplot as plt 
plt.plot(X[Y==0,0], X[Y==0,1], 'ob', label='Class 0')
plt.plot(X[Y==1,0], X[Y==1,1], 'sr', label='Class 1')
plt.legend(loc=2, numpoints=1)

plt.show()
{% endhighlight %}

which generates:

<div style="text-align: center">
    <img src="{{ site.baseurl }}/images/logreg-1.png" width="500px" height="426px">
</div>

Visually, we can see the data should be able to be separated by a line fairly well.

### Partial derivatives

We assume the parameters are independent. We assume $b$ is uniform with a large range (no regularization), and $w$ are gaussian with variance $1/\lambda$. So,

$$
\begin{align*}
    D_bl(w,b) &= \sum_{i=1}^n g(x^i|w,b) - y_i =: \sum_{i=1}^n (G-Y)_i\\
    D_{w_k}l(w,b) &= -\lambda w_k + \sum_{i=1} (g(x^i|w,b) - y^i)x_k^i
    D_wl(w,b) &=: -\lambda w + X(G-Y)
\end{align*}
$$

The definitions of the vectors, $G$ and $Y$, allow us to compute the gradient with respect to all of $w$ more efficiently using the matrix-vector product. Note that $\lambda$ is a free regularization parameter to be set. Finally, we take gradient ascent steps from some initial parameters using a fixed step size, $\eta$:

$$
\begin{align*}
    b &\leftarrow b + \eta \cdot D_bl(w,b) \\
    w &\leftarrow w + \eta \cdot D_wl(w,b)
\end{align*}
$$

Let's implement this:

{% highlight python %}
def gradient_ascent(w, b, lambda, eta, n_iters):
    for iter in range(n_iters):
        # G is P(Y=1|X) under the current parameters.
        G = 1 / (1. + np.exp(-b-np.dot(X,w)))
        # loss is the function we're maximizing
        loss = -lambda * np.log(w**2).sum() + np.log(G[Y==1]).sum() + np.log(1-G[Y==0]).sum()

        print "iteration:", iter, "| loss:", loss

        # Now, do gradient ascent.
        gmy    = G-Y
        grad_b = gmy.sum()
        grad_w = -lambda * w + np.dot(X,gmy)

        b += eta*grad_b
        w += eta*grad_w
{% endhighlight %}

