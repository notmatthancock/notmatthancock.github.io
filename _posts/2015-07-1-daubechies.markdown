---
published: false
layout: post
title: Construction of Daubechies Wavelet
tags: math wavelets
mathjax: true
---

The Daubechies wavelet constructs a wavelet which has smallest support for a given number of vanishing moments. Loosely speaking, the number of vanishing moments describes a wavelet's ability to represent smooth signals efficiently, while small support describes the manner (local vs global) in which the basis functions approximate. Wavelets can be constructed with these properties (among others) in mind.

---

#### Thereom (mallat, meyer):

If $\phi$ is the scaling function for a multiresolution analysis, then the so-called conjugate-mirror filter sequence:

$$
    h_n = \left\langle \frac{1}{\sqrt{2}} \phi\left( \frac{t}{2} \right), \phi(t-n) \right\rangle
$$

has discrete-time Fourier transform,

$$
    \hat{h}(w) = \sum_{n\in\mathbb{Z}} h_n e^{-inw}
$$

which satisfies:

 1. $|\hat{h}(w)|^2 + |\hat{h}(w+\pi)|^2 = 2$
 2. $\hat{h}(0) = \sqrt{2}$

Conversely, if we have a $2\pi$ perdiodic function, $\hat{h}(w)$, which satisfies:

 1. $|\hat{h}(w)|^2 + |\hat{h}(w+\pi)|^2 = 2$
 2. $\hat{h}(0) = \sqrt{2}$
 3. $\inf|\hat{h}| > 0$ on $[-\pi/2,\pi/2]$
 4. differentiable near $w=0$

then

$$
    \hat{\phi}(w) \prod_{p=0}^{\infty} \frac{\hat{h}(2^{-p}w)}{\sqrt{2}}
$$

is the Fourier transform of scaling function which generates a multiresolution analysis.

---

The following shows the relationship between the scaling function, conjugate-mirror filter, and the wavelet.

#### Theorem (mallat, meyer)

The Fourier transform of the wavelet associated with scaling function is given by:

$$
    \hat{\psi}(w) = \frac{1}{\sqrt{2}} e^{-i\frac{w}{2}} \hat{h}\left(\frac{w+2\pi}{2}\right)^* \hat{\phi}\left(\frac{w}{2}\right)
$$

---

A wavelet having $p$ vanishing moments means: $\langle t^k, \psi(t) \rangle = 0$ for $k=0,\ldots,p-1$. If a signal is smooth, and the wavelet has a sufficient amount of vanishing moments, then the magnitude of of the coefficients in the wavelet representation of $f$ are small at fine scales.

#### Theorem (vanishing moments)

The following two conditions are equivalent:

 * $\psi$ has $p$ vanishing momemnts
 * $\hat{h}^{(k)}(\pi) = 0$ for $k=0,1,\ldots,p-1$

---

The following shows the relationship between compact support of the scaling function, conjugate-mirror filter, and the wavelet.

#### Theorem (compact support)
$\phi$ has compact support if and only if $h$ has compact support. The supports are equal. If the support of $\phi$ is $[M,N]$, then the support of $\psi$ is $[(M-N+1)/2, (N-M+1)/2]$.

---

## Daubechies wavelet construction




A polynomial which satisfies:

$$
    x^pf(1-x) + (1-x)^pf(x) = 1 \tag{1}
$$

Let $g(x) = (1-x)^p f(x)$. This implies $f(x) = \frac{g(x)}{(1-x)^p}$. Since $f$ is a polynomial, this implies $g$ has a zero of order $p$ at $x=1$. So, $g^{(n)}(1) = 0, \;n=0,1,\ldots,p-1$. We can make the factorization:

$$
    g(x) = (1-x)^p \sum_{j=0}^{q} a_j x^j \tag{2}
$$

It's clear that the coefficients, $a_j$, are the coefficients of $f$. We assume for the moment that $f$ is some degree $q$ to be determined. How do we find the coefficients of $f$? Notice that differentiating condition $(1)$ $n$ times yields:

$$
    g^{(n)}(x) + (-1)^n g^{(n)}(1-x) = \delta[n]
$$

where $\delta[n]$ is one only if $n=0$ and $1$ otherwise. Plugging in $x=1$, we find:

$$
    g^{(n)}(0) = \delta[n], \; n=0,1,\ldots,p-1
$$

This yields $p$ linear equations. Thus, to have a unique solution, there must be exactly $p$ unknowns. In turn, this says that $q=p-1$, and $f$ must be degree $p-1$. With these constraints ($p$ vanishing moments), this is smallest degree $f$ can be.

Using $(2)$ and $n=0$, it's immediate that $a_0=1$. On the other hand, viewing $g(x) = r(x)s(x)$ with $r(x) = (1-x)^p$ and $s(x) = \sum_j= a_j x^j$, one can apply the [general Leibniz rule](https://en.wikipedia.org/wiki/General_Leibniz_rule) to find:

$$
    g^{(n)}(x) = \sum_{l=0}^n \sum_{j=n-l}^{p-1} \begin{pmatrix} n \\ l \end{pmatrix} \frac{p!}{(p-l)!} \frac{j!}{(j-(n-l))!} (-1)^l a_j  x^{j-(n-l)} (1-x)^{p-1}
$$

Thus,

$$
    g^{(n)}(0) = \sum_{l=0}^n \begin{pmatrix} n \\ l \end{pmatrix} \frac{p!(n-1)!}{(p-l)!} (-1)^l a_{n-l}
$$

This yields explicitly the set of $p$ linear equations:

$$
    \sum_{l=0}^n \begin{pmatrix} n \\ l \end{pmatrix} \frac{p!(n-1)!}{(p-l)!} (-1)^l a_{n-l} = \delta[n], \; n=0,1,\ldots,p-1 \tag{3}
$$

This forms a triangular linear system is where the diagonal is $1$, so the polynomial, $f$, satisfying $(1)$ exists and is unique. It is not difficult manipulate $(3)$ into a recurrence beginning with $a_0$. However, it turns out that there is nicer closed form expression for the coefficients.

### Proposition

$$
    a_n = \begin{pmatrix} p-1+n \\ n \end{pmatrix} \tag{4}
$$

---

#### Proof

Clearly, $a_0=1$ using the above. We use induction to show that $(3)$ holds for $n>0$ precisely when we use $(4)$. That is, we show:

$$
    \sum_{l=0}^n \begin{pmatrix} n \\ l \end{pmatrix} \frac{p!(n-l)!}{(p-l)!} (-1)^l \begin{pmatrix} p-1+n-l \\ n-l \end{pmatrix} = \sum_{l=0}^n \begin{pmatrix} p \\ l \end{pmatrix} (-1)^l \frac{(p-1+n-1)!}{(p-1)!} = 0
$$

holds for $n>0$. The base case holds:

$$
    \sum_{l=0}^1 \begin{pmatrix} p \\ l \end{pmatrix} (-1)^l \frac{(p-1)!}{(p-1)!} =  0
$$

Next, we show that

$$
    \sum_{l=0}^{n+1} \begin{pmatrix} n+1 \\ l \end{pmatrix} (-1)^l \frac{(p-l+n)!}{(p-l)!} = 0 \tag{5}
$$

under the induction hypothesis. First, split the sum:

$$
    (5) = \sum_{l=0}^n \begin{pmatrix} n+1 \\ l \end{pmatrix} (-1)^l \frac{(p-l+n)!}{(p-l)!} + (-1)^{n+1} \frac{(p-1)!}{(p-n-1)!} =: (a) + (b)
$$

Next, we use an identity sometimes called [Pascal's rule](https://proofwiki.org/wiki/Pascal%27s_Rule) to split the binomial term in $(a)$:

$$
    (a) = \sum_{l=0}^n \begin{pmatrix} n \\ l \end{pmatrix} (-1)^l \frac{(p-l+n)!}{(p-l)!} + \sum_{l=1}^n \begin{pmatrix} n \\ l-1 \end{pmatrix} (-1)^l \frac{(p-l+n)!}{(p-l)!} =: (c) + (d)
$$

First, we focus on $(c)$:

\begin{align*}
    (c) &= \sum_{l=0}^n \begin{pmatrix} n \\ l \end{pmatrix} (-1)^l \frac{(p-l+n-1)!}{(p-l)!} ((p+n) - l) \\
        &= (p+n) \sum_{l=0}^n \begin{pmatrix} n \\ l \end{pmatrix} (-1)^l \frac{(p-l+n-1)!}{(p-l)!} + \sum_{l=0}^n \begin{pmatrix} n \\ l \end{pmatrix} (-1)^l \frac{(p-l+n-1)!}{(p-l)!} (-l) \\
        &= 0 + \sum_{l=0}^n \begin{pmatrix} n \\ l \end{pmatrix} (-1)^l \frac{(p-l+n-1)!}{(p-l)!} (-l)
\end{align*}

The first term is $0$ due to the induction hypothesis. Next, let's look at $(d)$:

\begin{align*}
    (d) &= \sum_{l=1}^n \begin{pmatrix} n \\ l-1 \end{pmatrix} (-1)^l \frac{(p-l+n)!}{(p-l)!} \\
        &= -\sum_{l=0}^{n-1} \begin{pmatrix} n \\ l \end{pmatrix} (-1)^l \frac{(p-l)(p-l+n-1)!}{(p-l)!} \\
        &= -\sum_{l=0}^{n} \begin{pmatrix} n \\ l \end{pmatrix} (-1)^l \frac{(p-l)(p-l+n-1)!}{(p-l)!} + (-1)^n \frac{(p-n)(p-1)!}{(p-n)!} \\
        &= 0 + \sum_{l=0}^{n} \begin{pmatrix} n \\ l \end{pmatrix} (-1)^l \frac{(p-l+n-1)!}{(p-l)!}l + (-1)^n \frac{(p-n)(p-1)!}{(p-n)!}
\end{align*}

where the last step is again due the induction hypothesis. Wrapping up, we have that:

$$
    (c) + (d) = (-1)^n \frac{(p-1)!}{(p-n-1)!}
$$

So that:

$$
    (5) = (a) + (b) = 0
$$

which completes the proof.

--- 
