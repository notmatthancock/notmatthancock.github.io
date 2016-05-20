---
layout: post
title: What is Machine Learning?!
mathjax: true
tags:
- math
- pattern-recognition
---

In this post, I give a brief introduction to the binary classification problem in machine learning / pattern recognition. This problem is one particular instance of the "supervised learning" problem in machine learning, which itself is also a subset of the field of machine learning (arguably the most popular subset, however). I assume a familiarity with basic probability theory and statistics. Afterwards, I introduce the logistic regression model. In a separate post, I'll give a numerical example with Python of the logistic regression method.

## Probabilistic set-up

We have objects of two types that we'd like to classify automatically. The type of an object is called the **class** or **label** of the object. In the binary problem, objects can only have one of two possible labels. The labels are encoded numerically to either $1$ or $0$ (obviously not the only choice). Thus, we consider the label a Bernoulli random variable, $$Y \in \{0,1\}$$.

Next, we describe the object through some set of features or characteristics which we organize into a vector. Each object's characteristics are encoded by a random variable $X \in \mathbb{R}^p$, where $p$ is fixed number of characteristics we use to describe each object. One could think about $X$ as a subset of the total physical characteristics of an object that we've deemed suitable to assign a label, $Y$.

Now, without getting too philosophical, let's make the following assumptions:

1. Nature distributes the characteristics, $X$, randomly according to $P(X)$.
2. Labels, $Y$, are produced using the conditional distribution, $P(Y\|X)$.
3. The label, $Y$, depends only on the set of $p$ characteristics in $X$ and no other outside factors.

Knowing $P(Y\|X)$ is the golden ticket. This distribution contains all the information needed to make a decision about the label given an object's features. Of course, the problem is we don't know $P(Y\|X)$ (in fact, it's existence is only hypothetical under the assumptions above).

So what do we do? We define some model $g(X \| \theta)$ parameterized by $\theta \in \mathbb{R}^q$ where $q$ is the total number of parameters in the model. We want to interpret the output of $g$ as $P(Y=1\|X,\theta)$ so the range of $g$ should be normalized to $[0,1]$. Then finally, our hope is that:

$$
    g(x | \theta) = P(Y=1|X=x,\theta) \approx P(Y=1 | X=x)
$$

## Learning model parameters

Assume now that we have a sample of $n$ tuples: $(X^i, Y^i)$, $i=1,\ldots,n$. Each pair, $(X^i, Y^i)$, is identically distributed and independent conditioned on $\theta$. Call $\mathbf{X} = (X^1, \ldots, X^n)$ and $\mathbf{Y} = (Y^1, \ldots, Y^n)$. The idea is to assess the probability of the parameters, $\theta$, given the observations, $\mathbf{X}$ and $\mathbf{Y}$ and determine the maximum (or some acceptable local maximum). We begin by applying Bayes' rule:

$$
\begin{align*}
    P(\theta| \mathbf{X}, \mathbf{Y}) &= \frac{P(\mathbf{X},\mathbf{Y} | \theta)P(\theta)}{P(\mathbf{X},\mathbf{Y})} \\
    &\propto P(\mathbf{X},\mathbf{Y} | \theta) P(\theta) \\
    &= P(\theta)\prod_{i=1}^n P(X^i, Y^i | \theta) \\
    &= P(\theta)\prod_{i=1}^n P(Y^i | X^i, \theta) P(X^i|\theta) \tag{1} \\
\end{align*}
$$

At this point, we could potentially determine $\theta$ by maximizing over $(1)$ (or any of the forms above it). This is called the **maximum a posteriori** (MAP) estimate of $\theta$. On the other hand if we were to ignore the $P(\theta)$ term and maximize the right-hand side, the resulting estimate of $\theta$ is called the **maximum likelihood estimate** (MLE). The $P(\theta)$ term is the called **prior** or **regularization** term, and the absence of this term is essentially the case where $P(\theta)$ is uniform on some very large interval. Using either of these estimates require what is called a [generative model](https://en.wikipedia.org/wiki/Generative_model), which means we model all the terms on the right-hand side above. We are not using this type of model because we are only modelling $P(Y\|X,\theta)$ and perhaps $P(\theta)$.

In the field of machine learning / pattern recognition generative models are not used nearly as often as [discriminative models](https://en.wikipedia.org/wiki/Discriminative_model). A discriminative model only models the conditional distribution of the label, $Y$, given input, $X$. We are assuming this type of model. It derives an estimate of $\theta$ by assuming $P(X^i \| \theta) = P(X^i)$. This estimate is called the **conditional maximum likelihood** estimate. The regularization term may or may not be used. We have in this case that:

$$
\begin{align*}
    \text{(1)} &\propto P(\theta)\prod_{i=1}^n P(Y^i | X^i, \theta) \\
               &= P(\theta) \prod_{i=1}^n g(X^i|\theta)^{Y^i} (1-g(X^i |\theta))^{1-Y^i}  \\
\end{align*}
$$

where $g$ is finally introduced. Note that writing $g$ in the form of the previous expression explicitly depends on the fact that $g$ represents a Bernoulli random variable for fixed $X$, and that $Y$'s range is $\\{0,1\\}$.

So finally, given some concrete realizations of $\mathbf{X}$ and $\mathbf{Y}$, the model parameters are determined by:

$$
    \hat{\theta} = \arg\max_{\theta} \left\{ P(\theta) \prod_{i=1}^n g(x^i|\theta)^{y^i} (1-g(x^i |\theta))^{1-y^i} \right\}
$$

or equivalently:

$$
\begin{align*}
    \hat{\theta} &= \arg\max_{\theta} \left\{ \log(P(\theta)) + \sum_{i=1}^n y^i\log( g(x^i|\theta)) + (1-y^i)\log(1-g(x^i |\theta)) \right\} \\
    &=: \arg\max_{\theta}\left\{ l(\theta) \right\} \tag{2}
\end{align*}
$$

In this form, the log of the prior corresponds exactly with what's usually called $L^2$ or $L^1$ regularization if $\theta$ is assumed to be Gaussian or Laplacian respectively. For example if $\theta = (\theta_1, \theta_2, \ldots, \theta_q )$, and $\theta_j$ are independent Gaussian with zero mean and variance $1/\lambda$, then $\log(P(\theta)) \propto -\lambda \sum_j \theta_j^2$.

## Example: logistic regression

Logistic regression is a discriminative model which takes $q=p+1$ where $\theta = (b, w_1, \ldots, w_p)$. The $b$ term is often called the **bias** term. The model then assumes the form:

$$
    g(x|w,b) = \frac{1}{1+\exp\left(-b-\sum_{j=1}^p w_j x_j\right)} = \frac{1}{1+\exp\left(-b - w^Tx \right)} \tag{3}
$$

Recall that the set of points: $\\{ x \in \mathbb{R}^p : w^Tx + b = 0 \\}$ defines a hyperplane. In fact, we have that:

1. $g(x\|w,b) =   1/2 \Leftrightarrow w^Tx +b =   0$ 
2. $g(x\|w,b) \gt 1/2 \Leftrightarrow w^Tx +b \gt 0$ 
3. $g(x\|w,b) \lt 1/2 \Leftrightarrow w^Tx +b \lt 0$ 

Property 1 is why the hyperplane itself is also called the **decision boundary**. Essentially, $w^Tx + b$ measures the signed distance (up to scale of $w$) from the hyperplane. The exponential and the rest of the functional form of the logistic regression function, $g$, squash the signed distance values between $0$ and $1$.

The sign of the distance tells which class territory the point lives in according to the logistic regression model while the magnitude says how sure the classifier is of the label. So, for this model to perform well, the classes must be separated well by a hyperplane. Classes bound in a spiral would not be classified well by the logistic regression model, for instance.

Plugging $(3)$ into $(2)$ yields:

$$
    l(w,b) = \log(P(w,b)) + \sum_{i=1}^n y^i \log\left( \frac{1}{1+\exp\left(-b-w^Tx^i \right)} \right) + (1-y^i) \log\left( \frac{1}{1+\exp\left(b+w^Tx^i \right)} \right) 
$$

This function is concave so long as the logarithm of the prior term is concave. This is the case for independent Gaussian and independent Laplacian priors. The maximum of this function must be found via numerical methods. Partial derivatives are:

$$
\begin{align*}
    D_bl(w,b) &= D_b \log(P(w,b)) + \sum_{i=1}^n y^i - g(x^i|w,b) \\
    D_{w_k}l(w,b) &= D_{w_k} \log(P(w,b)) + \sum_{i=1}^n (y^i - g(x^i|w,b)) x_k^i
\end{align*}
$$

In [a separate post]({{ site.baseurl }}/2015/08/02/machine-learning-part-2-numerical-example.html), I go through a numerical example using Python.


### References
---

<div id="cite-1">
<sub>
[1]: Duda, Richard O., and Peter E. Hart. Pattern classification and scene analysis. Vol. 3. New York: Wiley, 1973.
</sub>
</div>

<div id="cite-2">
<sub>
[2]: Friedman, Jerome, Trevor Hastie, and Robert Tibshirani. The elements of statistical learning. Vol. 1. Springer, Berlin: Springer series in statistics, 2001.
</sub>
</div>

<div id="cite-3">
<sub>
[3]: Casella, George, and Roger L. Berger. Statistical inference. Vol. 2. Pacific Grove, CA: Duxbury, 2002.
</sub>
</div>
