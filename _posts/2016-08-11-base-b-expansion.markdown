---
layout: post
title: Existence proof for base-b expansion
tags:
- math
- analysis
mathjax: true
---
It's often taken for granted that we can expand a real number in a base of our choosing. For example, $0.1$, can be written in base-2 as:

$$
0.1 = 0.000110011001100 \ldots = 2^{-4} \times \sum_{n=0}^\infty a_k 2^{-k}
$$

where $a_0=a_1=1$, $a_2=a_3=0$, etc. In general, however, we would like to say we can expand any given real number in any integer base, $b$, greater than 1. This is what we'll show.

<br>
<hr>

**Theorem** Suppose $x \in (0,\infty)$, $b \in \\{2, 3, \ldots \\}$. Then, there exist both an integer, $e$, and a sequence $( a_n )_{n=0}^\infty$ with $a_n \in \\{0,1,\ldots,b-1\\}$ such that

$$
    b^e \sum_{n=0}^N a_n b^{-n} \to x, \;\; N \to \infty
$$

<hr>
<br>

**Proof**  The proof is constructive. Set

$$
    e = \lfloor \log_b(x) \rfloor
$$

and

$$
    a_n = \left\lfloor \left(\frac{x}{b^e} - \sum_{k=0}^{n-1} a_k b^{-k}\right) b^n \right\rfloor
$$

Loosely, the values arise by successively solving for $a_n$ in the partial sums, and then taking the floor of the resulting value. Denote the partial sums, $s_n = b^e\sum_{k=0}^n a_k b^{-k}$. The proof is completed in 3 parts, by proving

1. $0 \leq a_n < b$ for all $n$
2. $x-s_n > 0$ for all $n$.
3. $s_n \to x$.

Before proceeding, note that the inequalties $t-1 < \lfloor t \rfloor \leq t$ hold for all real $t$. These two inequalities will be used extensively.

### Proof of 1.

We proceed by induction.

By the inequalities mentioned above, we have $\log_b(x)-1 < e \leq \log_b(x)$ so that $0 \leq a_0 < b$ follows.

Next, supposing that $0 \leq a_n < b$, we have

$$
\begin{align*}
    a_{n+1} &> \left(\frac{x}{b^e} - \sum_{k=0}^n a_k b^{-k}\right)b^{n+1} -1 \\ 
            &= \left(\frac{x}{b^e} - \sum_{k=0}^{n-1} a_k b^{-k}\right)b^{n+1} -a_nb -1 \\ 
            &\geq \left\lfloor \left(\frac{x}{b^e} - \sum_{k=0}^{n-1} a_k b^{-k}\right)b^n \right\rfloor b -a_nb -1 \\ 
            &= a_nb -a_nb -1 = -1\\ 
\end{align*}
$$

So that, $a_{n+1} > -1$ or $a_{n+1} \geq 0$. Similarly,

$$
\begin{align*}
    a_{n+1} &\leq \left(\frac{x}{b^e} - \sum_{k=0}^n a_k b^{-k}\right)b^{n+1} \\ 
            &= \left(\frac{x}{b^e} - \sum_{k=0}^{n-1} a_k b^{-k}\right)b^{n+1} - a_nb \\ 
            &= \left(\frac{x}{b^e} - \sum_{k=0}^{n-1} a_k b^{-k}\right)b^{n+1} -b + b - a_nb \\ 
            &= \left( \left(\frac{x}{b^e} - \sum_{k=0}^{n-1} a_k b^{-k}\right)b^n -1 \right)b + b - a_nb \\ 
            &< \left\lfloor \left(\frac{x}{b^e} - \sum_{k=0}^{n-1} a_k b^{-k}\right)b^n \right\rfloor b + b - a_nb \\ 
            &= a_nb +b -a_n b = b
\end{align*}
$$

That is, $a_{n+1} < b$. Thus, $0 \leq a_n < b$ for all $n \geq 0$.

### Proof of 2.

Observe that for arbitrary $n$,

$$
\begin{align*}
    x - s_n &= x - b^e\sum_{k=0}^na_kb^{-k} \\
            &= b^e \left(\frac{x}{b^e} - \sum_{k=0}^na_kb^{-k} \right) b^nb^{-n} \\
            &\geq b^e \left\lfloor \frac{x}{b^e} - \sum_{k=0}^na_kb^{-k} b^n \right\rfloor b^{-n} \\
            &= b^e a_n b^{-n} \\
            &\geq 0 \\
\end{align*}
$$

### Proof of 3.

Now we show that $s_n \to x$.

First, fix $\epsilon > 0$. Then, by choosing $n$ such that $b^{e-n} < \epsilon$, we have

$$
\begin{align*}
    a_n &> \left(\frac{x}{b^e} - \sum_{k=0}^n a_k b^{-k}\right)b^n -1 \\ 
        &= \left(\frac{x}{b^e} - s_{n-1}\right)b^n -1 \\ 
        &= \frac{x - s_{n-1} - b^{e-n}}{b^{e-n}} \\ 
        &> \frac{x - s_{n-1} - \epsilon}{b^{e-n}} \\ 
\end{align*}
$$

Rearranging the final inequality, we have $x-s_n < \epsilon$.

This completes the proof.

## Testing the construction numerically
<hr>

Because the proof is constructive it directly translates to an algorithm for generating the base-b expansion of a given number. [Here's some code to do it.]({{ site.baseurl }}/code/py/base_b_expansion.py) Try it out:

{% highlight python %}
import base_b_expansion as bb

# Returns the value of the truncated sum, and the string representation.
print bb.expand_base_b(x=13.625, b=2, N=10)
=> (13.625, '1101.1010000') 

print bb.expand_base_b(x=0.1, b=2, N=10)
=> (0.0999755859375, '0.00011001100110')

print bb.expand_base_b(x=2**(0.5), b=3, N=13)
=> (1.4142134310299734, '1.1020112212220')
{% endhighlight %}
