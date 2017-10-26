---
layout: post
title: The Jaccard Overlap Score is Scale-Sensitive
area: notes
tags:
- math
- image-processing
mathjax: true
---

The Jaccard overlap score (or [Jaccard index](https://en.wikipedia.org/wiki/Jaccard_index)) between two sets $A$ and $B$ is the size of their intersection divided by the size of their union. In image segmentation, the set is usually represented by a discrete indicator, i.e., a boolean-valued matrix where one indicates the object (foreground) and zero indicates non-object (background). In this case, when $A,B \in \\{0,1\\}^{m \times n}$, the Jaccard overlap is

$$
    J(A,B) = \frac{\sum_{ij} a_{ij} \land b_{ij}}{\sum_{ij} a_{ij} \lor b_{ij}}
$$

where $\land$ and $\lor$ denote "logical and" and "logical or", respectively. This overlap score is between zero and one, where $J=0$ indicates no overlap between $A$ and $B$ and $J=1$ indicates perfect overlap. Usually, one of the matrices is considered to be the proposed, or approximate, segmentation, while the other is considered to be the exact, or "ground truth", segmentation of some object. So, the score $J(A,B)$ gives a measure of the quality of the proposed segmentation against the ground truth segmentation (the former usually provided by an algorithm and the latter usually provided by an expert).

The Jaccard overlap score is ubiquitous because it is simple to understand and implement, and provides a reasonable way to measure segmentation quality. Further, it continues to be popular *because* it is popular (i.e., it provides a standard metric to compare different methods in literature). Here, I show a particular aspect of the score: it is sensitive to the size of the ground truth segmentation. Let me make this precise.

Let $A,B \in \\{0,1\\}^{m \times n}$, and consider $B$ to be the "ground truth" segmentation. Now, let's suppose that matrix $A$ is formed by removing $p$ points from $B$ and by adding $q$ points to $A$ that are not in $B$. More precisely,

1. Set $A=B$.
2. Choose randomly a subset $P \subset \\{ (i,j) \, \| \, b_{ij}=1 \\}$ where $\|P\|=p$. Set $a_{ij}=0$ for all $(i,j)$ in $P$.
3. Choose randomly a subset $Q \subset \\{ (i,j) \, \| \, b_{ij}=0 \\}$ where $\|Q\|=q$. Set $a_{ij}=1$ for all $(i,j)$ in $Q$.

It's not too hard to see that this covers all proposed segmentations, $A$. Now, by 2., we have $\|A \cap B\| = \|B\| - p$, and by 3., we have $\|A \cup B\| = \|B\| + q$. This gives

$$
\begin{align*}
    J(A,B) &= \frac{|B| - p}{|B| + q} \\
           &= 1 - \frac{p+q}{|B| + q}
\end{align*}
$$

Note that when $p=q=0$ (i.e., $A=B$) we have that $J=1$ as expected. Otherwise, we miss the perfect score of 1 by a factor of $\frac{p+q}{\|B\| + q}$. This factor is increasing in both $p$ and $q$, if everything else is held fixed, which is expected: if we increase the number mismatched points ($p$ or $q$), we increase the factor $\frac{p+q}{\|B\| + q}$, and therefore decrease the overlap $J(A,B)$.

However, notice that the factor $\frac{p+q}{\|B\| + q}$ also depends on $\|B\|$, which is the size of the ground truth segmentation. Notice further that $\frac{p+q}{\|B\| + q}$ is decreasing in $\|B\|$, which means that for two segmentations where $\|B_1\| < \|B_2\|$ with $p$ and $q$ held fixed, then $\frac{p+q}{\|B_1\| + q} > \frac{p+q}{\|B_2\| + q}$.

In other words, even though $A_1$ and $A_2$ have the same number of pixel-wise errors ($p+q$), if $B_1$ is smaller than $B_2$, then we will have $J(A_1, B_1) < J(A_2, B_2)$.

This is something to be aware of while using this score. If you are segmenting objects over a large range of sizes, you might observe higher variability in the Jaccard overlap score for smaller objects because as shown above, it takes less pixel-wise errors to produce larger changes in overlap score for smaller objects.

#### Extras: Foreground vs background disagreements and the effect on the Jaccard score

Here's something additional to ponder. Given the choice, which is better in terms of the Jaccard overlap score: (a) setting a point in $A$ which is zero in $A$ and one in $B$ to one (i.e., reducing $p$ to $p-1$), or (b) setting a point in $A$ that is one in $A$ and zero in $B$ to zero (i.e., reducing $q$ to $q-1$)?

The answer is (a), because the inequality,

$$
    \frac{|B| - (p-1)}{|B| + q} > \frac{|B| - p}{|B| + (q-1)}
$$

follows from

1. $p+q > 1$ <small>(which is true under the assumption that $p,q \geq 1$)</small>
2. $\|B\| \geq p$ <small>(which is true because $p$ can be at most $\|B\|$)</small>
3. $\|B\|+q > 1$ <small>(which is true if $\|B\| \geq 1$)</small>

This means if there's a point where $a_{ij}=0$ and $b_{ij}=1$ and if there is separate point where $a_{st}=1$ and $b_{st}=0$, then we produce a larger increase in the Jaccard overlap by "flipping the bit" where $a_{ij}$ to 1 rather than setting $a_{st}$ to 0.

This is a somewhat of a surprising result. For example, consider the situation where $a_{ij}=1$ everywhere except $a_{st}=0$ at a single point where also $b_{st}=1$. The above says that we produce a larger increase in Jaccard overlap by setting $a_{st}=1$, rather than by switching any of the places in $A$ that equal to one to a zero, despite the fact that there are probably many more places where zeros must be switched to ones.

How much do we have to reduce $q$ to catch up with the overlap increase that results from reducing $p$ by one? If you fiddle with the inequalities, you find that we must reduce $q$ by at least $\frac{\|B\|+q}{\|B\|-(p-1)}$ (which is greater than 1), in order to produce the same increase in Jaccard overlap score as reducing $p$ by one.

For example, suppose the image is $101^2$ pixels, and $B$ indicates a square of size $21^2$ pixels. Consider the situation above where $A$ is ones everywhere except in a single place where $B$ is zero. In this case, $\|B\| = 21^2$, $q = 101^2 - 21^2$, and $p=1$. Then, we have to reduce $q$ by at least 24 (i.e., set 24 of the bits in $A$ to zero where $B$ is also zero) in order to produce the same increase in overlap score that results from simply from reducing $p$ to zero (i.e., setting $A$ to one in the only place it is zero).

The situation is less dramatic in a more realistic situation. For example, instead of $A$ being nearly all ones, suppose it is a square of ones centered on $B$ that is a single pixel too large, i.e., a square of ones size $23^2$. Suppose a single pixel on the interior of $A$ is zero when it should be one. Now, in this case, $\|B\|=21^2$, $p=1$, but now $q = 4\cdot 21  + 4$. So then $\frac{\|B\|+q}{\|B\|-(p-1)} \approx 1.2$, which says that we have to reduce $q$ by at least 2 to see the same increase that reducing $p$ by one produces.
