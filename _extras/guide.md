---
layout: page
title: "Instructor Notes"
permalink: /guide/
---

# Intro


 * introduce everyone
 * get attendees to introduce themselves
 * etherpad link http://board.net/p/scwaber-2018-11-21

 
# HPC background

What is a cluster

why use one:
* more memory
* faster/more processors
* specialist software
* leave stuff running

show cluster diagram

explain nodes vs cores

introduce SCW
RSEs
history with HPCW
current state
application process 


# Logging in

`ssh username@sunbird.swansea.ac.uk` or `ssh username@hawklogin.cf.ac.uk`

`sinfo`

`slurmtop`

## Exercises

* Setup account
* Logging in
* Run sinfo 


# Moving Data
`sftp username@sunbird.swansea.ac.uk` or `sftp  username@hawklogin.cf.ac.uk`
Show filezilla

Scratch dirs in /scratch/username

## Exercises

* run df -h
* run myquota
* copy a file

# Running Jobs

## Interactive jobs
Explain account and reservation codes. Export SBATCH_ACCOUNT/RESERVATION or SALLOC_ACCOUNT/RESERVATION
`salloc -n 1 --ntasks-per-node=1 --account=SCW1380 --reservation=SCW1380_X` 
`srun --pty -n 1 /bin/bash`
`squeue`

## Batch jobs

`nano batchjob.sh`

Copy example batch job to batchjob.sh
Explain #! and comments

`sbatch batchjob.sh`
explain job id
`cat hostname.out.<jobid>`
`cat hostname.err.<jobid>`

### Overriding sbatch

add sleep 70 to script
resubmit
show time limit error
run `sbatch --time 0-0:2 batchjob.sh`

### Cancelling jobs
`scancel`

### Listing jobs that have Running
`sacct`

## Exercises 
* Using sbatch

## Running multiple jobs with srun

This runs multiple copies of the same thing within a job. Lets us use multiple nodes.

`#!/bin/bash --login`

`###`

`#SBATCH --job-name=hostname`

`#SBATCH --output=hostname.out.%J`

`#SBATCH --error=hostname.err.%J`

`#SBATCH --time=0-00:01`

`#SBATCH --mem-per-cpu=10`

`#SBATCH --ntasks=2`

`#SBATCH --ntasks-per-node=1`

`#SBATCH --nodes=2`
`#SBATCH --account=SCW1380_X`
`#SBATCH --reservation=SCW1380_X`

`###`

`srun /bin/hostname`

run it with sbatch.

`sbatch job.sh`

## Job Arrays
`sbatch --array=0-2 batchjob.sh`
`squeue`
show output files

## Monitoring jobs
`sacct -j JOBID --format=JobID,JobName,ReqMem,MaxRSS,Elapsed`

Talk about mem, time, nodes and core allocations.

## Partitions
`sinfo` show different partitions
`sbatch -p <part name> batchjob.sh`

## Email alerts
`#SBATCH --mail-user=abc1@aber.ac.uk`
`#SBATCH --mail-type=ALL`

## Exercises
* email output
* job arrays

# Modules

`python3` - command not found
`module avail`
`module load hpcw python/3.5.1`

## python modules

`pip3 install --user <mod>`
`pip3 install --user sklearn`

`from sklearn import datasets`
`digits = datasets.load_digits()`
`print(digits.data)`


## Exercises

* run a python script

# HPC Best Practice

See webpage

# Optimising for Parallel Processing

crude way:

`#!/bin/bash --login`

`###`

`#job name`

`#SBATCH --job-name=test`
`#SBATCH --output=test.out.%J`
`#SBATCH --error=test.err.%J`
`#SBATCH --time=0-00:01`
`#SBATCH --ntasks=3`
`#SBATCH --account=SCW1380_X`
`#SBATCH --reservation=SCW1380_X`

`###`

`command1 &`

`command2 &`

`command3 &`

what if command1/2/3 take different amounts of time to run? 
We've got CPUs allocated but we aren't using them. Want to keep usage near to 100%

What if command4 needs to run after command1/2/3.

GNU parallel is a powerful program designed to run multiple jobs on a single node.
module called parallel contains it.

parallel can read input from a pipe and apply a command to each line of input

`ls | parallel echo {1}`

`ls | parallel echo` 

alternate syntax for same thing

`parallel echo {1} ::: $(ls)`

${1} means first argument, separate each argument with another :::

`parallel echo {1} {2} ::: 1 2 3 ::: a b c`


Use parallel on Nelle's pipeline from Unix Shell lesson.

`wget http://swcarpentry.github.io/shell-novice/data/data-shell.zip`
`unzip data-shell.zip`
`cd data-shell/north-pacific-gyre/2012-07-03/`

We used to process this with a for loop in series.
Switch to parallel 

`ls NENE*[AB].txt | parallel goostats {1} stats-{1}` 




parallel.sh:

`#!/bin/bash --login`

`###`

`#SBATCH --ntasks 4                     #Number of processors we will use`

`#SBATCH --nodes 1                      #request everything runs on the same node`

`#SBATCH -o output.%J              #Job output`

`#SBATCH -t 00:00:05               #Max wall time for entire job`
`#SBATCH --account=SCW1380_X`
`#SBATCH --reservation=SCW1380_X`

`###`

`module load hpcw`

`module load parallel`

`srun="srun -n1 -N1" `

`parallel="parallel -j $SLURM_NTASKS --joblog parallel_joblog"`

`ls NENE*[AB].txt | $parallel "$srun bash ./goostats {1} stats-{1}"`


submit it:

`sbatch parallel.sh`

sacct will show 15 subjobs. 

parallel_joblog shows how long each took to run.

## Summary

* GNU Parallel lets a single Slurm job start multiple subprocesses
* This helps to use all the CPUs on a node effectively.

# Estimation of Pi on a single core

## Buffon's Needle

Monte carlo method for estimating Pi
drop points randomly on a circle/quadrant

draw a circle, take a quadrant
drop m random points on a quadrant
n is number inside the circle 

     4*m
Pi = ---
      n
      
see python implementation of this

x^2 + y^2 < 1 means inside the circle

## Profilers

write code which works, measure performance, optimise

profilers tell us how long each line of code takes

python line_profiler is one of these

install with 

`module load hpcw python/3.5.1`

`pip3 install --user line_profiler`

we have to tell the profiler which function to profile with @profile tag
put this before def main(): 
refactor so there's a main function 

try to find an empty head node to do this, ssl003 is a good bet

run profiler:

`~/.local/bin/kernprof -l ./serial_numpi.py 50000000`

output stored in 

serial_numpi_profiled.py.lprof

view it with

`python3 -m line_profiler serial_numpi.py.lprof`

estimate_pi function takes 100% of the time

remove annotation from main and move it to estimate_pi

repeat profiling

inside_circle now shows 100%

move profiling to there and repeat again

generating random numbers takes about 60% of the time. this is our prime target for optimisation.

## Exercises

* profiling Exercises
* pair/group exercise on optimisation

## Summary

* Profilers can analyse the runtime of your code.
* The estimate of pi spends most of it's time while generating random numbers.
* The estimation of pi with the Monte Carlo method is a compute bound problem because pseudo-random numbers are just algorithms. There's no major I/O going on.

# Parallel estimation of Pi

Showed previously random number generation was 60-70% of time.
show profiler output again. 

`python3 -m line_profiler serial_numpi.py.lprof`

X and Y are indepedendent variables (see first figure in notes)
can generate them in parallel

random numbers genreated with numpy, similar to

`a = np.random.uniform(size=10)`

`b = np.random.uniform(size=10)`

`c = a + b`

a and b are lists, final line is concatenating the two lists

`for i in range(len(a)):`
`    c[i] = a[i] + b[i]`

achieves same thing, but makes it clearer whats going on

we could generate each pair of X/Y values in parallel (see second figure in notes)

## Exercises

Data independence 1,2,3

## Amdahl's law

What is the overall speedup of a program when some of it is done in paralle?

           1
S = ---------------
    (1 - p) + (p/s)
    
p = portion of program sped up
s = speedup achieved


parallel calculation of x and y
occupied 70% of time
speedup of 2 in that time
             1
S = ----------------
    (1 - 0.7) + (0.7/2) 

S = 1.538


## Exercises

* Compute the speedup with 4 parts 
* Always go parallel right?

## More Amdhal's law

Show Amdahl's law graph

we can't infinitely parallelise, limit to number of cores etc
additional limits from I/O and memory bottlenecks

in the example Lola splits data into partitions, see figure

PyMP and OpenMP, parallel loops
simpler than threads 
can also use the multiprocessing library in python

explain shared vs private variables, locking

run pymp version `python3 ./pymp_numpi.py 1000000000`

time it `time python3 ./pymp_numpi.py 1000000000`
compare to serial one `time python3 ./serial_numpi.py 1000000000`

## Exercises

* thought exercises on what can be parallelised (x2)

## Summary

* "Amdahl's law is a description of what you can expect of your parallelisation efforts."
* "Use the profiling data to calculate the time consumption of hot spots in the code."
* "The generation and processing of random numbers can be parallelized as it is a data parallel task."
* "Time consumption of a single application can be measured using the `time` utility."
* "The ratio of the run time of a parallel program divided by the time of the equivalent serial implementation, is called speed-up."

# MPI

Message Passing Interface

passes messages between cluster nodes

useful when problem is too big for one node

copy example to mpi_hostname.sh

`sbatch -n 4 mpi_hostname.sh`

repeat with more cores

`sbatch -n 16 mpi_hostname.sh`

order of output might be a bit random. Merging of the file done by synchronising on each line. 

MPI libraries available for lots of languages including C/C++, Fortran and Python 

Install mpi4py

`module load mpi`

`module load hpcw python/3.5.1`

`pip3 install --user mpi4py`

create py_mpi_hostname.sh with example contents

submit with `sbatch -n 16 py_mpi_hostname.sh`

## Exercises 

* run date with mpirun
* upgrade print_hostname.py to include timestamps

## MPI calculation of Pi

MPI size tells us how many instances of the code are running

rank tells us which instance we are. Usually the instance with rank 0 does the coordination.

`comm = MPI.COMM_WORLD`

code to get size/rank:

`comm.Get_size()`

`comm.Get_rank()`

Every line of code running will be in parallel in a different MPI process, possibly on a different node

Rank 0 will often do something different to other ranks. Show hello world and pi example in notes.

MPI's scatter function will scatter an array in equal parts across all instances. 
The gather function will gather data from all instances and merge them back together. 

In example final computation of Pi done on rank 0 only.

run it, make sbatch script with `time mpirun python3 mpi_numpi.py 1000000000`

run with `sbatch -n 48 mpi_pi.sh`

Investigate time output

Show performance graphs

MPI vs PyMP performance, different nodes. Try PyMP as an sbatch job.

## Summary

* "The MPI driver `mpirun` sends compute jobs to a set of allocated computers. It works with Slurm or the system scheduler to do this."
* "The MPI software then executes these jobs on the remote hosts and synchronizes their state/memory."
* "MPI assigns a rank to each process, usually the one with a rank of zero does the coordination"
* "MPI can be used to split a task into components and have several nodes run them."
