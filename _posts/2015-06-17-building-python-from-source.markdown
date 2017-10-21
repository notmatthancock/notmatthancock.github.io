---
layout: post
title: Building Python from Source
area: notes
tags:
- software
- python
- guides
mathjax: false
---

The following are notes for building and installing tcl/tk/python 2.7.6 from source into a custom directory.

The following was done on Cent OS 6.5 and uses bash syntax (version > 4). It also assumess a shell variable, `LOCAL`, is defined where you keep your files in your home directory. Mine is defined in my `.bashrc` as `export LOCAL=$HOME/local`. Don't forget that when you update your `.bashrc` file, you must restart bash or run `source ~/.bashrc` to make changes available.

Let's get started.

We should build and install Tcl/Tk before python. This library is especially important if you plan to install matplotlib - a great plotting library for python. You can skip this step if you don't plan on installing matplotlib. In fact, you can still install matplotlib without Tcl/Tk, and you'll have all the functionality to save figures to file, but no X11 graphical interactivity. There's other X11 backends for matplotlib such as `pygtk`. However, `pygtk` has a laundry list of dependencies that are a pain to install.

First, let's do Tcl:

{% highlight bash %}
wget http://prdownloads.sourceforge.net/tcl/tcl8.4.20-src.tar.gz
tar xvf tcl8.4.20-src.tar.gz
cd tcl8.4.20-src
./configure --prefix=$LOCAL
make
make install
{% endhighlight %}

And Tk next:

{% highlight bash %}
wget http://prdownloads.sourceforge.net/tcl/tk8.4.20-src.tar.gz
tar xvf tk8.4.20-src.tar.gz
cd tk8.4.20-src
./configure --prefix=$LOCAL
make
make install
{% endhighlight %}

OK that was easy. Now let's install python. You should have shell variable, `PYPATH`, defined that specifies where python will be installed. For instance, in my `.bashrc`, I have: `export PYPATH=$LOCAL/lib/python/2.7.6`.

{% highlight bash %}
wget --no-check-certificate https://www.python.org/ftp/python/2.7.6/Python-2.7.6.tgz
tar xvf Python-2.7.6.tgz
cd Python-2.7.6.tgz
./configure --prefix=$PYPATH --enable-shared --with-tcltk-includes="-I$LOCAL/include" --with-tcltk-libs="-L$LOCAL/lib -ltcl8.4 -L$LOCAL/lib -ltk8.4"
make
make install
{% endhighlight %}


Update (or define if they aren't already) the following in your `.bashrc`:

{% highlight bash %}
export LIBRARY_PATH=$PYPATH # $PYPATH:$LIBRARY_PATH if already defined
export LD_LIBRARY_PATH=$PYPATH # similar ^
{% endhighlight %}

Now we need to create some symlinks:

{% highlight bash %}
export PATH=$LOCAL/bin:$PATH # append only if PATH is defined. change dir as you manage.
ln -s $PYPATH/bin/python $LOCAL/bin/python
ln -s $PYPATH/bin/python-config $LOCAL/bin/python-config
{% endhighlight %}

Now check

{% highlight bash %}
python -V # should return 2.7.6
{% endhighlight %}

Finally, you should install pip. Pip is a package manager for python libraries that, when possible, makes installing and book-keeping python extensions a breeze. Install as follows:

{% highlight bash %}
wget --no-check-certificate https://raw.github.com/pypa/pip/master/contrib/get-pip.py
python get-pip.py
ln -s $PYPATH/pip $LOCAL/bin/pip
ln -s $PYPATH/easy_install $LOCAL/bin/easy_install
{% endhighlight %}

Great. Now you can install some other great packages easily:

{% highlight bash %}
pip install cython # for compiling python into c
pip install nose # unit tests
pip install memory_profiler # great tool for tracking the line-by-line memory behavior of a script
{% endhighlight %}

Numpy and SciPy are two important libraries for mathematical / scientific computing. You should build them from source rather than installing using pip so that way you can point to your system's LAPACK/BLAS/ATLAS libraries. I won't talk about doing that here.
