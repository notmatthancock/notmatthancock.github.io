---
layout: post
title: Starting a Background Process and Logging it
area: notes
tags:
- software
- bash
---

I can never remember the syntax for starting a background process and piping both stdout and stderr to a file, so this post is mostly a personal note.

Let's say we a driver program that's a python script `main.py` that prints its progress to stdout, and maybe it errors, too. We'd like to set the driver program running in the background, but we'd also like to view its progress and note any errors. We'd also like to record the process id so we can kill the driver program if we'd like to. This is accomplished by a couple of lines of bash, say in a file `main.sh`:

{% highlight bash %}
python -u main.py > log.txt 2>&1 &
printf "$!" > pid.txt
{% endhighlight %}

The `-u` flag forces output from the python script to be unbuffered. The `2>&1` after piping to the log file (via `> log.txt`) ensures that both standard print statements and errors both get sent to the log file. Having a long process that errors but having no idea of what error was made is a hopeless position.

We can monitor the progress (assuming `main.py` is actually printing relevant progress information to stdout) by `tail log.txt` or `tail -n 100 log.txt` to get the latest 100 lines, for example.

The second line records the process id of the python script, so if necessary we can kill it by executing something like

{% highlight bash %}
kill `cat pid.txt`
{% endhighlight %}
