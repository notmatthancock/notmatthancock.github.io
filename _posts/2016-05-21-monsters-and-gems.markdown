---
layout: post
title: Monsters and gems riddle
area: notes
tags:
- math
- probability
- riddles
mathjax: true
---
[Another riddle from 538!](http://fivethirtyeight.com/features/can-you-slay-the-puzzle-of-the-monsters-gems/) This one goes like this:

> A video game requires you to slay monsters to collect gems. Every time you slay a monster, it drops one of three types of gems: a common gem, an uncommon gem or a rare gem. The probabilities of these gems being dropped are in the ratio of 3:2:1 — three common gems for every two uncommon gems for every one rare gem, on average. If you slay monsters until you have at least one of each of the three types of gems, how many of the most common gems will you end up with, on average?

# Simulation

It's pretty straight-forward to whip together a simulation with python:

{% highlight python %}
import numpy as np
from scipy.stats import rv_discrete

pk = np.array([1/2., 1/3., 1/6.])
xk = np.arange(pk.shape[0])

dist = rv_discrete(values=(xk, pk))

def trial():
    counts = np.zeros(3)
    n=0
    while min(counts) == 0:
    counts[dist.rvs()] += 1.
    n+=1
    return n, counts

if __name__ == '__main__':
    n_trials = 10000
    print "Average common gem count in %d trials is: %.2f" \
    % (n_trials, np.mean([trial()[1][0] for _ in range(n_trials)]))
{% endhighlight %}

Running the above, I get:

`Average common gem count in 10000 trials is: 3.64` 

Unfortunately, the pen-and-paper solution is not as easy, but this gives an estimate of what we should expect.

# Solution

Let $N \in \\{3, 4, \ldots \\}$ be the number of monsters slain required to obtain at least one gem of each type. This is a random variable with some distribution to be determined. On the other hand, given a number of monsters slain, say $n$, the number of each type of gems of each type obtained follows a [multinomial distribution](https://en.wikipedia.org/wiki/Multinomial_distribution), with parameters, $n$, $p_1=\frac{1}{2}$, $p_2=\frac{1}{3}$, and $p_3=\frac{1}{6}$. We can call the gem count variable, $X$, noting that $X \in \mathbb{N}^3$ and $X_1 + X_2 + X_3 = n$. At the component level,

1. $X_1$ is the number of common gems obtained, after $n$ monsters have been slain.
2. $X_2$ is the number of uncommon gems obtained, after $n$ monsters have been slain.
3. $X_3$ is the number of rare gems obtained, after $n$ monsters have been slain.

So, to find the expected number of common gems obtained when we have slain enough monsters to obtain at least one of each gem type, we must find:

$$
    E_N\left[E_{X_1|N} \left[ X_1 \right] \right] \tag{1}
$$

The inner expectation is straight-forward because [the marginal distribution of a multinomial is a binomial](http://www.math.uah.edu/stat/bernoulli/Multinomial.html). Thus $E_{X_1\|N} X_1 = Np_1 = N\frac{1}{2}$ since the [expectation of a binomial random variable](https://en.wikipedia.org/wiki/Binomial_distribution) with parameters $n$ and $p$ is $np$.

The expectation, $(1)$, is thus $\frac{1}{2} E[N]$. This requires that we determine the distribution of $N$. Remember that $N$ represents the number of monsters slain required to obtain at least one of each type of gem. To determine this, note that:

$$
    \{N > n\} \Leftrightarrow \{X_1=0 \text{ or } X_2=0 \text{ or } X_3=0\} \tag{2}
$$

The events on the right-hand-side of $(2)$ are not mutually exclusive, so using the [inclusion-exclusion principle](https://en.wikipedia.org/wiki/Inclusion%E2%80%93exclusion_principle#In_probability), we have:

$$
\begin{align*}
    P(X_1=0 \text{ or } X_2=0 \text{ or } X_3=0) = &P(X_1=0) \\
                                                   +&P(X_2=0) \\
                                                   +&P(X_3=0) \\
                                                   -&P(X_1=0,X_2=0) \\
                                                   -&P(X_1=0,X_3=0) \\ 
                                                   -&P(X_2=0,X_3=0) \\ 
                                                   +&P(X_1=0,X_2=0,X_3=0)
\end{align*}
$$

At first, this might look complicated, but it works out pretty cleanly. The first three terms are just binomial random variables, so:

1. $P(X_1=0) = \left(1-\frac{1}{2}\right)^n = \left(\frac{1}{2}\right)^n$
2. $P(X_2=0) = \left(1-\frac{1}{3}\right)^n = \left(\frac{2}{3}\right)^n$
3. $P(X_3=0) = \left(1-\frac{1}{6}\right)^n = \left(\frac{5}{6}\right)^n$

On the other hand, if any two gem counts are zero, the third must be equal to $n$, so:

1. $P(X_1=0, X_2=0) = P(X_3=n) = \left(\frac{1}{6}\right)^n $
2. $P(X_1=0, X_3=0) = P(X_2=n) = \left(\frac{1}{3}\right)^n $
3. $P(X_2=0, X_3=0) = P(X_1=n) = \left(\frac{1}{2}\right)^n $

Lastly, the event that all three gem counts are zero never occurs, so its probability is zero.

Thus, we have:

$$
\begin{align*}
    P(N > n) = &\left(\frac{1}{2}\right)^n + \left(\frac{2}{3}\right)^n + \left(\frac{5}{6}\right)^n \\
              -&\left(\frac{1}{6}\right)^n - \left(\frac{1}{3}\right)^n - \left(\frac{1}{2}\right)^n \\
             = &\left(\frac{2}{3}\right)^n - \left(\frac{1}{3}\right)^n + \left(\frac{5}{6}\right)^n - \left(\frac{1}{6}\right)^n
\end{align*}
$$

In the above, note that $P(N > n) = 1$ for any $n < 3$ by definition, and in fact, the above formula holds for $n \geq 1$, but not $n \leq 0$.

So we have the distribution, and now we need the expectation. By [writing the terms in the expectation](http://math.stackexchange.com/a/64227/28479), we have:

$$
    E[N] = \sum_{n=3}^{\infty} n P(N = n) = 2P(N>2) + \sum_{n=2}^{\infty} P(N > n) \tag{3}
$$

The probability that $N$ is greater than $2$ is of course, $1$, while:

$$
    \sum_{n=2}^{\infty} P(N > n) = \sum_{n=2}^{\infty} [r_1^n - (1-r_1)^n] + [r_2^n - (1-r_2)^n]
$$

where $r_1 = 2/3$ and $r_2=5/6$. In both cases, we have that

$$
    \sum_{n=2}^{\infty} r^n - (1-r)^n = \frac{r^2}{1-r} - \frac{(1-r)^2}{r}
$$

so that when the smoke finally clears:

$$
    E[N] = 2 + \frac{124}{30} + \frac{7}{6} = 2 + 5.3 = 7.3
$$

**Finally**, the average common gem count when we have slain enough monsters to obtain at least one gem of each type is:

<div style="color:red">
$$
    p_1 E[N] = 0.5 \cdot 7.3 = 3.65 \text{ common gems}
$$
</div>
