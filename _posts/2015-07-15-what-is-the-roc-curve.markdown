---
published: false
layout: post
title: What is the ROC curve?!
tags: math statistics pattern-recognition
mathjax: true
---

The [ROC curve](https://en.wikipedia.org/wiki/Receiver_operating_characteristic) as well as the area under the curve (AUC) score are frequently used in binary classification to characterize the quality of an automatic classifier. In this post, I want to define these things from an analytic perspective, and show how the usually definitions are simply empirical estimates of the analytic expressions. This is important because it shows what the ROC curve and AUC score *really are* &mdash; it's not just pedantry. Furthermore, it's much easier to derive properties of the ROC curve and AUC score with an analytic form for it, rather than attempting to say things about particular instances of empirical estimates of them.

## Probabilistic preliminaries 

Assume we have objects, $X$, who have associated binary labels, $$Y \in \{0,1\}$$, and we devise a classifying mechanism which assigns a score, $T \in \mathbb{R}$, given an object, $X$. We make the assignment $1$ when $T \gt t$ and $0$ when $T \leq t$ for some chosen $t$. Let's for the sake of concreteness suppose that:

$$
    X|Y=y \; \sim  \; N(u_y, 1)
$$

Now, let's make some assumptions. Let's assume we observe $n$ objects such that each (label, score) tuple is independent identically distributed (iid), i.e. $$\{ (Y_i, T_i) \}_{i=1}^n$$ are iid.

### The event of a [true,false][positive, negative]

We define $T \gt t \cap Y=1$ as a **true positive** event or $TP$. Similarly, $T \leq t \cap Y=0$ is defined as a **false negative** event or $FN$. The other two possibilities are defined similarly, i.e. **false positive** ($FP$) and **true negative** ($TN$). 

We define the sum of all realizations of $TP$ events from the sample as:

$$
    tp := \sum_{i=1}^n \mathbb{I}( t_j > t \cap y_j=1 )
$$

where $\mathbb{I}$ is the indicator function that's $1$ if the argument is true and $0$ otherwise, and $t_j, y_j$ are realizations of the random variables, $T_j, Y_j$. Again, $tn$, $fp$, and $fn$ are defined similarly. 

So now because of the iid assumption, we can make the estimates:

$$
    P(TP) \approx tp / n, \;\; P(FP) \approx fp / n \text{etc...}
$$

So we when we measure empircal accuracy, we are really making the estimate:

$$
    P(TP \cup TN) \approx \frac{tp+tn}{n}
$$

However, accuracy alone isn't always the best measure of success. In fact, measures of "false positivity" and "false negativity" are critical in areas like medicine.


### Conditional classifier predictions (true and false positive rates)

In some ways, the true positive (and related) events are strange to consider. A true positive event considers when two events occur **together**: 1) the event that classifier's output given an object is above a threshold and 2) the even that the label for the object is $1$. However, we know that an object has a label whether or not the classifier has assigned a score to it. Nature has given the object a label. Hence, it makes a bit more sense to condition on the label of the object, i.e. consider the distribution of the classifier threshold given a particular label.

We call the following the **true positive rate** ($TPR$), and **false positive rate** ($FPR$) respectively:

$$
    TPR := P(T \gt t | Y=1), \;\; FPR := P(T \gt t | Y=0)
$$

$TPR$ also goes by **sensitivity** or **recall**. It is the probability of the event that the classifier will predict $1$ given that the true label is $1$. $FPR$ is also known as the **fall-out** or 1-**specificity**. It's the probability that the classifier will predict label $1$ given that the true label is $0$.

Empirically, we estimate $TPR$ and $FPR$ simply using the definition of conditional probability:

$$
\begin{align*}
    TPR &= \frac{P(T \gt t, Y=1)}{P(Y=1)} \\
        &= \frac{P(T \gt t, Y=1)}{P(T \gt t, Y=1) + P(T \leq t, Y=1)} \\
        &\approx \frac{tp/n}{tp/n + fn/n} \\
        &= \frac{tp}{tp+fn}
        &\\
        &\\
    \text{similarly,}\;\;FPR &\approx \frac{fp}{fp+tn}
\end{align*}
$$

Actually, the $TPR$ and $FPR$ are usually (in every case that I've seen) just *defined* as the empirical estimate of the probability. I've taken the opposite view point.

## The ROC curve

The ROC curve is simply the parametric curve:

$$
    r(t) =
    \begin{bmatrix}
        P(T \gt t | Y=0) \\
        P(T \gt t | Y=1)
    \end{bmatrix}
$$

Note that $$\lim\limits_{t \to -\infty} r(t) = \begin{bmatrix} 1 \\ 1 \end{bmatrix}$$ and $$\lim\limits_{t \to \infty} r(t) = \begin{bmatrix} 0 \\ 0 \end{bmatrix}$$.

## AUC score

Assume $T\|Y=0$ and $T\|Y=1$ have pdfs. Then the area under the ROC curve, $r(t)$, is:

$$
    \int_{\tau} P(T \gt t | Y=1) p(t | Y=0) dt
$$
