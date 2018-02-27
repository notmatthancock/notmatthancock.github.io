---
layout: post
title: Referencing LaTex objects from Matplotlib
area: notes
tags:
- software
- matplotlib
- latex
---

Recently, I wanted to reference an equation in a LaTeX document from a figure created using [matplotlib](https://matplotlib.org/). Luckily, matplotlib has a PGF backend that makes this possible. Here's an example:


**`main.tex`:**

{% highlight latex %}
\documentclass[12pt]{article}

\usepackage{amsmath}
\usepackage{pgf}

\begin{document}

\begin{equation}
\label{eq:foo}
    e^{i\pi} + 1 = 0
\end{equation}

\begin{figure}[h]
    \centering
    \resizebox{3in}{3in}{
        \input{figure.pgf}
    }
    \caption{This is the caption.}
\end{figure}

\end{document}
{% endhighlight %}

So we have an labeled equation, and we'd like to create the file `figure.pgf` so that the equation can be referenced in the figure.

**`make_figure.py`:**
{% highlight python %}
import numpy as np
import matplotlib as mpl
mpl.use('pgf')
pgf_with_custom_preamble = {
"text.usetex": True,    # use inline math for ticks
"pgf.rcfonts": False,   # don't setup fonts from rc parameters
"pgf.preamble": [
    "\\usepackage{amsmath}",         # load additional packages
]
}
mpl.rcParams.update(pgf_with_custom_preamble)
import matplotlib.pyplot as plt

plt.figure(figsize=(4,4))
plt.plot(np.random.randn(10), label="Equation \\eqref{eq:foo}")
plt.grid(ls=":")
plt.legend(loc=2)
plt.savefig("figure.pgf", bbox_inches="tight")
{% endhighlight %}

I've borrowed some of the settings from the [matplotlib pgf page](https://matplotlib.org/users/pgf.html). You can apparently get quite deep into the pgf settings in matplotlib (see [here](http://bkanuka.com/articles/native-latex-plots/) for example).

Now, finally run,

{% highlight bash %}
python make_figure.py
pdflatex main
pdflatex main
{% endhighlight %}

That not a typo --- you must run `pdflatex` twice to get the references correct. Here's the output:

<div style="text-align:center">
    <img style="border: 1px solid #333; margin: 0 auto;" src="{{ site.baseurl }}/images/matplotlib-latex-ref.png">
</div>
