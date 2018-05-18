---
title: "Parallel Processing Introduction"
author: "Colin Sauze"
questions:
 - "How do you split up a job to process data in parallel"
objectives: 
 - "Understand how to partition data"
 - "Understand the difference between using multiple processors/cores and multiple nodes"
 - "Understand the use of multithreading and OpenMP to use multiple cores"
---


# 

Use pymp for OpenMP like functionality in Python. OpenMP is a library that makes parallelising code very easy. 



Install with

~~~
$ pip3 install --user pymp-pypi
~~~
{: .bash}


~~~
#!/usr/bin/env python3
import sys

import numpy as np

#from multiprocessing import cpu_count, Pool
import pymp

np.random.seed(2017)

def inside_circle(total_count):

    x = np.float32(np.random.uniform(size=total_count))
    y = np.float32(np.random.uniform(size=total_count))

    radii = np.sqrt(x*x + y*y)

    filtered = np.where(radii<=1.0)
    count = len(radii[filtered])

    return count 

def estimate_pi(total_count):

    #count is a shared variable that all threads will store their results in
    count = pymp.shared.array((4,), dtype='float32')
    with pymp.Parallel(4) as p:
        for i in p.range(0,4):
            local_count = inside_circle(total_count/4.0)

            #we have to obtain a lock to access count, only one thread can do this at a time
            #the reason we have each thread use local count is so that we don't hold the lock
            #for the whole time inside_circle is running
            with p.lock:
                count[i] = local_count

    total_count = sum(count)
    return (4.0 * sum(counts) / total_count)

if __name__=='__main__':

    n_samples = 10000
    if len(sys.argv) > 1:
        n_samples = int(sys.argv[1])

    my_pi = estimate_pi(n_samples)

    print("[pymp version] required memory %.3f MB" % (n_samples*sizeof*3/(1024*1024)))
    print("[using 4 cores ] pi is %f from %i samples" % (my_pi,n_samples))
~~~
{: .python}