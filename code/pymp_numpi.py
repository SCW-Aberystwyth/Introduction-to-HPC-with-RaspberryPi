#!/usr/bin/env python3
import sys

import numpy as np

import pymp
import math
#needed to get core core
from multiprocessing import cpu_count


np.random.seed(2017)

def inside_circle(total_count):

    x = np.float32(np.random.uniform(size=total_count))
    y = np.float32(np.random.uniform(size=total_count))

    radii = np.sqrt(x*x + y*y)

    filtered = np.where(radii<=1.0)
    count = len(radii[filtered])

    return count 

def estimate_pi(total_count,core_count):

    #count is a shared variable that all threads will store their results in
    count = pymp.shared.array((core_count,), dtype='int32')
    
    #start of pymp parallel section, request a thread for each core 
    with pymp.Parallel(core_count) as p:
        #this for loop will be executed in parallel
        for i in p.range(0,core_count):
            local_count = inside_circle(int(total_count/core_count))

            #we have to obtain a lock to access count, only one thread can do this at a time
            #the reason we have each thread use local count is so that we don't hold the lock
            #for the whole time inside_circle is running
            with p.lock:
                count[i] = local_count

    return (4.0 * sum(count) / total_count)

if __name__=='__main__':

    n_samples = 10000
    
    #get the number of cores, assuming we have hyperthreading the real number is half the number that gets reported
    core_count = int(cpu_count())
    
    #let the user specify the number of samples as the first command line argument
    if len(sys.argv) > 1:
        n_samples = int(sys.argv[1])
        
    #let the user specify core count as the second argument
    if len(sys.argv) > 2:
        core_count = int(sys.argv[2])

    my_pi = estimate_pi(n_samples,core_count)

    print("[pymp version] [using %d cores ] pi is %f from %i samples" % (core_count,my_pi,n_samples))
