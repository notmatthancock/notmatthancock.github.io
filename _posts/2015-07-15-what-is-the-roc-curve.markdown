---
published: false
layout: post
title: What is the ROC curve?!
tags: math statistics pattern-recognition
mathjax: true
---

The [ROC curve](https://en.wikipedia.org/wiki/Receiver_operating_characteristic) as well as the area under the curve (AUC) score are frequently used in binary classification to characterize the quality of an automatic classifier. I want to look at the ROC curve and AUC score from an analytic perspective in order to derive empirical estimates and show some important properties of the two.


## Probabilistic preliminaries 

Let's consider the factors at play:

* **Input** &mdash; Assume we have some objects. We describe each object through a vector containing some its features, $X \in \mathbb{R}^p$. One could think of this as the features are just a subset of characteristics of the object and that nature has produced these characteristics according to some distribution.
* **Label** &mdash; These objects have an associated label, $$Y \in \{0,1\}$$. The labels are produced through $X$ and possibly other unknown factors in some unknown or complex way. Here, I like to think some subset of mankind produces the labels through the characteristics, $X$, as well taking possibly other non-included characteristics into account.
* **Classifier Output** &mdash; We produce an automatic classifying mechanism that produces an output, $T \in \mathbb{R}$. This output is based only on the input $X$, and is used to predict the corresponding label by fixing some **threshold**, $t$. If $T \gt t$, we say the classifier predicts label $Y=1$. Otherwise, it picks label $0$.  

Assume we have objects<sup><a href="#note-1">\[1\]</a></sup> who have associated binary labels, $$Y \in \{0,1\}$$, and we devise a classifying mechanism which assigns a score, $T \in \mathbb{R}$, given an object. We make the assignment $1$ when $T \gt t$ and $0$ when $T \leq t$ for some chosen $t$. The value $t$ is sometimes called a threshold.

Duda & Hart <sup>1</sup> discuss the ROC curve in a similar way to this. There, however, they assume 

Furthermore, let us assume we have a sample of $n$ (label, score) tuples such that the total sample is independent identically distributed (iid), i.e. $$\{ (Y_i, T_i) \}_{i=1}^n$$ are iid.

### Events of label/output agreements and disagreements

Define $T \gt t \cap Y=1$ as a **true positive** event or $TP$. Similarly, $T \leq t \cap Y=0$ is defined as a **false negative** event or $FN$. The other two possibilities are defined similarly, i.e. events of **false positive** ($FP$) and **true negative** ($TN$). 

We define the sum of all realizations of $TP$ events from the sample as:

$$
    tp := \sum_{i=1}^n \mathbb{I}( t_j > t \land y_j=1 )
$$

where $\mathbb{I}$ is the indicator function that's $1$ if the argument is true and $0$ otherwise, and $t_j, y_j$ are realizations of the random variables, $T_j, Y_j$. Again, $tn$, $fp$, and $fn$ are defined similarly. 

So now because of the iid assumption, we can make the estimates:

$$
    P(TP) \approx tp / n, \;\; P(FP) \approx fp / n, \;\; \text{etc...}
$$

So we when we measure empirical accuracy, we are really making the estimate:

$$
    P(TP \cup TN) \approx \frac{tp+tn}{n}
$$

However, accuracy alone isn't always the best measure of success. Measures of "false positivity" and "false negativity" are critical in areas like medicine.

### Conditional classifier predictions

We just saw that accuracy essentially measures the probability of co-occurrence of agreement between the classifier and label. A similar but different question to ask pertains to the classifiers prediction *conditioned* on the label taking a particular value. So for instance, we might be interested in the probability that the classifier takes a value above the threshold, $t$, *given that* the label is $1$.

We call the following the **true positive rate** ($TPR$), and **false positive rate** ($FPR$):

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

$TPR$ and $FPR$ are usually just *defined* as the empirical estimate of the probability. As I stated in the intro, I've taken the opposite view point.

## The ROC curve

After laying the previous groundwork, the ROC curve is simply the parametric curve:

$$
    r(t) =
    \begin{bmatrix}
        P(T \gt t | Y=0) \\
        P(T \gt t | Y=1)
    \end{bmatrix}
$$

This is a curve in the $FPR-TPR$ plane.

### Properties of the ROC curve

1. $\lim\limits_{t \to -\infty} r(t) = \begin{bmatrix} 1 \\\\ 1 \end{bmatrix}$
2. $\lim\limits_{t \to +\infty} r(t) = \begin{bmatrix} 0 \\\\ 0 \end{bmatrix}$
3. $r(t)$ is non-increasing component-wise

So the ROC curve starts from the point $(1,1)$, ends at $(0,0)$, and is confined to the unit square: $[0,1] \times [0,1] \subset \mathbb{R}^2$. The last statement says the curve can't loop back on itself. 

### The worst curve?

Consider the following:

<div style="text-align: center">
$r(t)$ is a straight line from $(1,1)$ to $(0,0)$.

$$\Leftrightarrow$$

$$P(T \gt t | Y=1) = P(T \gt t | Y=0)$$

$$\Leftrightarrow$$

$T,Y$ are independent.
</div>

<br>

So a straight line from $(1,1)$ to $(0,0)$ is the worst possible situation. It means the classifier's prediction is independent of the label! Ideally, our classifier would predict the label, $Y$, exactly. This would mean that $T$ is completely dependent on $Y$, i.e. knowing $T$ means knowing $Y$ (perfect classification).  

### The best curve?

Consider a curve which travels straight from $(1,1)$ to $(0,1)$, and then straight from $(0,1)$ to $(0,0)$. If the curve travels along this path, then we must be able to partition the real line into disjoint intervals:

* $A_1 = (-\infty, a)$
* $A_2 = (a, b)$
* $A_3 = (b,c)$
* $A_4 = (c, \infty)$

where $a \lt b \lt c$ such that:

* $t \in A_1 \Rightarrow P(T \gt t \| Y=0) = P(T \gt t \| Y=0) = 1$.
* $t \in A_2 \Rightarrow P(T \gt t \| Y=0) \in (0,1), \; P(T \gt t \| Y=1) = 1$.
* $t \in A_3 \Rightarrow P(T \gt t \| Y=0) = 0, \; P(T \gt t \| Y=1) \in (0,1)$.
* $t \in A_4 \Rightarrow P(T \gt t \| Y=0) = P(T \gt t \| Y=1) = 0 $.

In other words, the two conditional distributions are *completely separated*.

## AUC score

Assume $T\|Y=0$ and $T\|Y=1$ have pdfs. Then the area under the ROC curve, $r(t)$, is:

$$
    \int_{\tau} P(T \gt t | Y=1) p(t | Y=0) dt
$$

<br>
<br>

---

### Footnotes

<div id="note-1">
<sub>
1: I'm using the phrase "given an object" in a purposefully vague way. Typically, however, the object is a vector of features $X$, and the classifier produces its output based on this feature vector. So you could imagine two distributions: $Y|X$ and $T|X$. $Y|X$ is unknown or complex, and we try to capture its essence through the created classifier.

Since we're only concerned with quantifying the performance of the classifier, not producing one, I just drop the notion of $X$ because it clutters the notation and forces additional independence assumptions. We just assume $T$ is produced through $X$, and $T$ is scalar value used to make a decision about $Y$.
</sub> 
</div>
