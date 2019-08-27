---
title: "Profiling Single Core Performance"
teaching: 20
exercises: 40
questions:
- "How do I find the portion of a code snipped that consumes the longest time?"
objectives:
- "Perform an estimation of pi using only one CPU core."
- "Measure the run time of the serial implementation for this estimate of pi."
- "Find the line of code in a python program that took the longest."
keypoints:
- "Each programming language typically provides tools called profilers with which you can analyse the runtime of your code."
- "The estimate of pi spends most of it's time while generating random numbers."
- "The estimation of pi with the Monte Carlo method is a compute bound problem because pseudo-random numbers are just algorithms."
---

Lola Lazy is told that her predecessors all worked on the same project. A high performance calculation that is able to produce a high precision estimate of Pi. Even though calculating Pi can be considered a solved problem, this piece of code is used at the institute to benchmark new hardware. So far, the institute has only acquired larger single machines for each lab to act as work horse per group. But currently, need for distributed computations has arisen and hence a distributed code is needed, that yields both simplicity, efficiency and scalability. 

The algorithm was pioneered by _Georges-Louis Leclerc de Buffon_ in _1733_. 

![Estimating Pi with Buffon's needle]({{ page.root }}/fig/estimate_pi.svg)

Overlay a unit square over a quadrant of a circle. Throw `m` random number pairs and count how many of the pairs lie inside the circle (the number pairs inside the circle is denoted by `n`). `Pi` is then approximated by: 

~~~
     4*m
Pi = ---
      n
~~~

The implementation of this algorithm using `total_count` random number pairs in a nutshell is given in the program below:

~~~
import numpy

np.random.seed(2000)

def inside_circle(total_count):
    
    x = np.float32(np.random.uniform(size=total_count))
    y = np.float32(np.random.uniform(size=total_count))

    radii = np.sqrt(x*x + y*y)

    filtered = np.where(radii<=1.0)
    count = len(radii[filtered])
    
    return count 
    
def estimate_pi(total_count):

    count = inside_circle(total_count)
    return (4.0 * count / total_count) 

~~~
{: .python}

For generating pseudo-random numbers, we sample the uniform probability distribution in the default floating point interval from `0` to `1`. The `sqrt` step is not required directly, but Lola includes it here for clarity. `numpy.where` is used obtain the list of indices that correspond to radii which are equal or smaller than `1.0`. At last, this list of indices is used to filter-out the numbers in the `radii` array and obtain its length, which is the number Lola are after.

Lola finishes writing the pi estimation and comes up with a [small python script]({{ page.root }}/code/serial_numpi.py). You can download this to your account by running:

~~~
$ wget {{ page.root }}/code/serial_numpi.py
~~~

Then launch it from the command line:

~~~
$ python3 serial_numpi.py 10000000
~~~
{: .bash}

~~~
[serial version] required memory 114.441 MB
[serial version] pi is 3.141582 from 10000000 samples
~~~
{: .output}

Although this doesn't take long to complete the answer isn't very accurate. Lola suspects that using more samples in the code will improve accuracy, but she already used 114 MB of memory and the Raspberry Pi only has 512MB or 1024GB. She think that 150,000,000 samples would give a better answer but estimates this will need over 2GB of memory. So she decides to parallelize this algorithm first so that it can exploit multiple cores (and their attached memory) that the cluster has to offer. 

## Premature Optimisation is the root of all evil!

Before venturing out and trying to accelerate a program, it is utterly important to find the hot spots of it by means of measurements. For the sake of this tutorial, we use the [line_profiler](https://github.com/rkern/line_profiler) of python. Your language of choice most likely has similar utilities.

to install the profiler, please issue the following commands. These load the python module, enabling the pip3 command and then install the module using pip3. 

~~~
$ pip3 install --user line_profiler
~~~
{: .bash }

The profiler can be started with the command 

~~~
$ ~/.local/bin/kernprof 
~~~
{: .bash}

Note that on systems where pip can install to system directories the kernprof (or kernprof-3) command will be available without specifying a path.

> ## Profilers
>
> Each programming language typically offers some open-source and/or free tools on the web, with which you can profile your code. Here are some examples of tools. Note though, depending on the nature of the language of choice, the results can be hard or easy to interpret. In the following we will only list open and free tools:
>
> - python: [line_profiler](https://github.com/rkern/line_profiler), [prof](https://docs.python.org/3.6/library/profile.html)
> - java script: [firebug](https://github.com/firebug/firebug)
> - ruby: [ruby-prof](https://github.com/ruby-prof/ruby-prof)
> - C/C++: [xray](https://llvm.org/docs/XRay.html), [perf](https://perf.wiki.kernel.org/index.php/Main_Page), 
> - R: [profvis](https://github.com/rstudio/profvis)
{: .callout }

Next, you have to annotate your code in order to indicate to the profiler what you want to profile. For this, we add the `@profile` annotation to a function definition of our choice. If we don't do this, the profiler will do nothing.

Lets annotate the main function by changing:

~~~
def main():
~~~

to 

~~~
@profile
def main():
~~~

With this trick, we can make sure that we profile the entire application. Note, that this is a necessity when using `line_profiler`. Let's save this to `serial_numpi_annotated.py`. Now lets run the program with the profiler:

~~~
$ ~/.local/bin/kernprof -l ./serial_numpi.py 10000000
[serial version] required memory 114.441 MB
[serial version] pi is 3.141582 from 10000000 samples
Wrote profile results to serial_numpi.py.lprof

~~~
{: .bash }

You can see that the profiler just adds one line to the output, i.e. the last line. In order to view, the output we can use the `line_profile` module in python:

~~~
$ python3 -m line_profiler serial_numpi_profiled.py.lprof
Timer unit: 1e-06 s

Total time: 2.07893 s
File: ./serial_numpi_profiled.py
Function: main at line 24

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
    24                                           @profile
    25                                           def main():
    26         1            2      2.0      0.0      n_samples = 10000
    27         1            1      1.0      0.0      if len(sys.argv) > 1:
    28         1            3      3.0      0.0          n_samples = int(sys.argv[1])
    29                                           
    30         1      2078840 2078840.0    100.0      my_pi = estimate_pi(n_samples)
    31         1           11     11.0      0.0      sizeof = np.dtype(np.float32).itemsize
    32                                           
    33         1           50     50.0      0.0      print("[serial version] required memory %.3f MB" % (n_samples*sizeof*3/(1024*1024)))
    34         1           23     23.0      0.0      print("[serial version] pi is %f from %i samples" % (my_pi,n_samples)
~~~

Aha, as expected the function that consumes 100% of the time is `estimate_pi`. So let's remove the annotation from `main` and move it to `estimate_pi`:

~~~
    return count

@profile
def estimate_pi(total_count):

    count = inside_circle(total_count)
    return (4.0 * count / total_count)

def main():
    n_samples = 10000
    if len(sys.argv) > 1:
~~~

And run the same cycle of record and report:

~~~
$ kernprof-3 -l ./serial_numpi_annotated.py 10000000
[serial version] required memory 114.441 MB
[serial version] pi is 3.141728 from 10000000 samples
Wrote profile results to serial_numpi_annotated.py.lprof
$ python3 -m line_profiler serial_numpi_profiled.py.lprof
Timer unit: 1e-06 s

Total time: 2.0736 s
File: ./serial_numpi_profiled.py
Function: estimate_pi at line 19

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
    20                                           @profile
    21                                           def estimate_pi(total_count):
    22                                           
    23         1    3122882.0 3122882.0    100.0      count = inside_circle(total_count)
    24         1         43.0     43.0      0.0      return (4.0 * count / float(total_count))

~~~
{: .output }

Ok, one function to consume it all! So let's rinse and repeat again and annotate only `inside_circle`.

~~~
@profile
def inside_circle(total_count):

    x = np.float32(np.random.uniform(size=total_count))
    y = np.float32(np.random.uniform(size=total_count))

    radii = np.sqrt(x*x + y*y)

    filtered = np.where(radii<=1.0)
    count = len(radii[filtered])

    return count
~~~

And run the profiler again:

~~~
$ kernprof-3 -l ./serial_numpi_annotated.py 10000000
[serial version] required memory 114.441 MB
[serial version] pi is 3.141728 from 10000000 samples
Wrote profile results to serial_numpi_annotated.py.lprof
$ python3 -m line_profiler serial_numpi_profiled.py.lprof
Timer unit: 1e-06 s

Total time: 2.04205 s
File: ./serial_numpi_profiled.py
Function: inside_circle at line 7

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
     7                                           @profile
     8                                           def inside_circle(total_count):
     9                                           
    10         1       749408 749408.0     36.7      x = np.float32(np.random.uniform(size=total_count))
    11         1       743129 743129.0     36.4      y = np.float32(np.random.uniform(size=total_count))
    12                                           
    13         1       261149 261149.0     12.8      radii = np.sqrt(x*x + y*y)
    14                                           
    15         1       195070 195070.0      9.6      filtered = np.where(radii<=1.0)
    16         1        93290  93290.0      4.6      count = len(radii[filtered])
    17                                           
    18         1            2      2.0      0.0      return count
~~~

So generating the random numbers appears to be the bottleneck as it accounts for 37+36=73% of the total runtime time. 
So this is a prime candidate for acceleration.



