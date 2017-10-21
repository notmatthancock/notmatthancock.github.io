---
layout: post
title: Compiling multiple modules with f2py
area: notes
tags:
- software
- fortran
- f2py
- python
- guides
mathjax: false
---

For an intro to `f2py` [see here]({{ site.baseurl }}/2017/02/10/calling-fortran-from-python.html).

It's possible to combine multiple Fortran modules into a single shared library to be used by Python using `f2py`. It's actually pretty easy, but I'm writing a note about it because I'll likely forget how to do it in the future.

Let's suppose we have two modules, `one.f90` and `two.f90`. `one` uses `two`, and we only explicitly want to use the functions in `one` from Python.

For example, `one.f90` might contain:

{% highlight fortran %}
module one
use two

contains

function onefunc(x) result(y)
    real(8) :: x,y
    y = twofunc(x)
    y = twofunc(y)
end function

end module
{% endhighlight %}

... while in `two.f90`:

{% highlight fortran %}
module two
implicit none

contains

function twofunc(x) result(y)
    real(8) :: x,y
    y = x*x
end function

end module
{% endhighlight %}

To compile, execute:

{% highlight bash %}
gfortran -c two.f90
f2py -c two.f90 one.f90 -c one
{% endhighlight %}

Now, check that it works in python
{% highlight python %}
>>> from one import one
>>> one.onefunc(3)
>>> # 81.0
{% endhighlight %}
