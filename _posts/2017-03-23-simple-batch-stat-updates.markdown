---
layout: post
title: Batch updates for simple statistics
area: notes
tags:
- math
- statistics
- pattern-recognition
mathjax: true
comments: true
---

It's typical in many optimization problems in data analysis to standardize your data by subtracting off the empirical mean and dividing by the empirical standard deviation. However, in "online" situations where the data is acquired one at a time or in batches, it's only possible to compute these statistics over the data observed up to that point. Further, it might not be desirable to store all the observations and re-compute the mean and standard deviation each time new data is acquired. There are simple formulas to update the existing mean and standard deviation to reflect the new data without storing all the observations.

Suppose we've observed $m$ observations, $x_i, \; i=1,\ldots,n$, so far, and we obtain a new "batch" of $n$ observations, $x_i \; i=m+1, \ldots, m+n$. Now denote,

$$
\begin{align}
    \mu   &= \frac{1}{m+n} \sum_{i=1}^{m+n} x_i \\
    \mu_m &= \frac{1}{m} \sum_{i=1}^{m} x_i \\
    \mu_n &= \frac{1}{n} \sum_{i=m+1}^{m+n} x_i
\end{align}
$$

Equation (1) is the desired updated mean, which we **don't** want to compute as a sum over all observations. (2) is the current empirical mean, and (3) is the empirical mean of the new data batch. Yes, I realize I should write, $\hat{\mu}$, $\bar{x}$, or some such notation since the mean is empirical. But I'm not going to. Anyhow, from some simple calculations, we have that,

$$
\boxed{ \mu = \frac{m}{m+n} \mu_m + \frac{n}{m+n} \mu_n}
$$

In other words, the updated mean is a linear combination of the mean over the old data and the mean over new data, yielding a simple recursive update.

Now let's consider the empirical variances:

$$
\begin{align*}
    \sigma^2   &= \frac{1}{m+n} \sum_{i=1}^{m+n} (x_i - \mu)^2 \\
    \sigma_m^2 &= \frac{1}{m} \sum_{i=1}^{m} (x_i - \mu_m)^2 \\
    \sigma_n^2 &= \frac{1}{n} \sum_{i=m+1}^{m+1} (x_i - \mu_n)^2
\end{align*}
$$

Observe that

$$
\begin{align*}
    \sigma^2 &= \frac{1}{m+n} \sum_{i=1}^{m+n} x_i^2 - \mu^2 \\
    \frac{1}{m} \sum_{i=1}^{m} x_i^2 &= \sigma_m^2 + \mu_m^2 \\
    \frac{1}{n} \sum_{i=m+1}^{m+n} x_i^2 &= \sigma_n^2 + \mu_n^2
\end{align*}
$$

so that

$$
\boxed{\begin{align*}
\sigma^2 &= \frac{m}{m+n} (\sigma_m^2 + \mu_m^2) + \frac{n}{m+n} (\sigma_n^2 + \mu_n^2) - \mu^2 \\
         &= \frac{m}{m+n}\sigma_m^2 + \frac{n}{m+n} \sigma_n^2 + \frac{mn}{(m+n)^2} (\mu_m - \mu_n)^2
\end{align*}}
$$

The update is a linear combination of the observed variances plus a correction by the means.

Note that, initially, we can set $m = \mu_m = \sigma_m^2 = 0$, and the formulas all work out. Also note that these are fine to use for vectors, since these statistics are computed component-wise.

### Testing it out

Let's write a simple class for storing the mean and standard deviation of the examples observed. Write a file call "statsrecorder.py":

{% highlight python %}
import numpy as np

class StatsRecorder:
    def __init__(self, data=None):
        """
        data: ndarray, shape (nobservations, ndimensions)
        """
        if data is not None:
            data = np.atleast_2d(data)
            self.mean = data.mean(axis=0)
            self.std  = data.std(axis=0)
            self.nobservations = data.shape[0]
            self.ndimensions   = data.shape[1]
        else:
            self.nobservations = 0

    def update(self, data):
        """
        data: ndarray, shape (nobservations, ndimensions)
        """
        if self.nobservations == 0:
            self.__init__(data)
        else:
            data = np.atleast_2d(data)
            if data.shape[1] != self.ndimensions:
                raise ValueError("Data dims don't match prev observations.")

            newmean = data.mean(axis=0)
            newstd  = data.std(axis=0)

            m = self.nobservations * 1.0
            n = data.shape[0]

            tmp = self.mean

            self.mean = m/(m+n)*tmp + n/(m+n)*newmean
            self.std  = m/(m+n)*self.std**2 + n/(m+n)*newstd**2 +\
                        m*n/(m+n)**2 * (tmp - newmean)**2
            self.std  = np.sqrt(self.std)

            self.nobservations += n
{% endhighlight %}

Now in a separate script, say "test_statsrecorder.py", write:

{% highlight python %}
import numpy as np
import statsrecorder as sr

rs = np.random.RandomState(323)

mystats = sr.StatsRecorder()

# Hold all observations in "data" to check for correctness.
ndims = 42
data = np.empty((0, ndims))

for i in range(1000):
    nobserv = rs.randint(10,101)
    newdata = rs.randn(nobserv, ndims)
    data = np.vstack((data, newdata))

    # Update stats recorder object
    mystats.update(newdata)

    # Check stats recorder object is doing its business right.
    assert np.allclose(mystats.mean, data.mean(axis=0))
    assert np.allclose(mystats.std, data.std(axis=0))

{% endhighlight %}

You should observe nothing after running the scripts, which is exactly what should happen since we are asserting that our online tallies of mean and standard deviation agree with the same computation if all the observations were stored.
