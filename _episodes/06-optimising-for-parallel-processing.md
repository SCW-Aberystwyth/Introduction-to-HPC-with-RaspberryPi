---
title: "Optimising for Parallel Processing"
author: "Colin Sauze"
date: "December 2017"
questions: 
 - ""
objectives: 
 - "Understand how to use GNU Parallel to run multiple programs from one job"
keypoints:
 - "GNU Parallel lets a single Slurm job start multiple subprocesses"
 - "This helps to use all the CPUs on a node effectively."
---


# Optimising for Parallel Processing

## Running a job on multiple cores

By default most programs will only run one job per node, but all SCW/HPCW nodes have multiple CPU cores and are capable of running multiple processes at once without (much) loss of performance. 

A crude way to achieve this is to have our job submission script just run multiple processes and background each one with the `&` operator.

~~~
#!/bin/bash --login
###
#job name
#SBATCH --job-name=test
#SBATCH --output=test.out.%J
#SBATCH --error=test.err.%J
#SBATCH --time=0-00:01
#SBATCH --ntasks=3
###

command1 &
command2 &
command3 &
~~~
{: bash}

This will run command1,2 and 3 simultaneously. It also requests 3 cores with the ntasks option.

This method has its limits if we want to run multiple tasks after the first ones have completed. Its possible, but scaling it will be harder.

### GNU Parallel

GNU Parallel is a utility specially designed to run multiple parallel jobs. It can execute a set number of tasks at a time and when they are complete run more tasks.

GNU Parallel can be loaded a module called "parallel". Its syntax is a bit complex, but its very powerful. 

First lets create a job submission script and call it `parallel.sh`.

~~~
#!/bin/bash --login
#SBATCH -n 12                     #Number of processors in our pool
#SBATCH -o output.%J              #Job output
#SBATCH -t 00:00:05               #Max wall time for entire job

module load parallel

# Define srun arguments:
srun="srun -n1 -N1 --exclusive" 
# --exclusive     ensures srun uses distinct CPUs for each job step
# -N1 -n1         allocates a single core to each task

# Define parallel arguments:
parallel="parallel -N 1 --delay .2 -j $SLURM_NTASKS --joblog parallel_joblog --resume"
# -N 1              is number of arguments to pass to each job
# --delay .2        prevents overloading the controlling node on short jobs
# -j $SLURM_NTASKS  is the number of concurrent tasks parallel runs, so number of CPUs allocated
# --joblog name     parallel's log file of tasks it has run
# --resume          parallel can use a joblog and this to continue an interrupted run (job resubmitted)

# Run the tasks:
$parallel "$srun /bin/bash ./runtask.sh arg1:{1}" ::: {1..32}
# in this case, we are running a script named runtask, and passing it a single argument
# {1} is the first argument
# parallel uses ::: to separate options. Here {1..32} is a shell expansion defining the values for
#    the first argument, but could be any shell command
#
# so parallel will run the runtask script for the numbers 1 through 32, with a max of 12 running 
#    at any one time
#
# as an example, the first job will be run like this:
#    srun -N1 -n1 --exclusive ./runtask arg1:1
~~~
{: bash}


Now lets define a sciprt called `runtask.sh`, this is the script we want parallel to actually run. All it does is wait a random amount of time and output some information about the job on screen. 

~~~
#!/bin/bash

# this script echoes some useful output so we can see what parallel and srun are doing

sleepsecs=$[($RANDOM % 10) + 10]s

# $1 is arg1:{1} from parallel, it will be a number between 0 and 32
# $PARALLEL_SEQ is a special variable from parallel. It the actual sequence number of the job regardless of the arguments given
# We output the sleep time, hostname, and date for more info&gt;
echo task $1 seq:$PARALLEL_SEQ sleep:$sleepsecs host:$(hostname) date:$(date)

# sleep a random amount of time
sleep $sleepsecs
~~~
{: bash}


Now lets go ahead and run the job by using `sbatch` to submit `parallel.sh`. 

~~~
sbatch parallel.sh
~~~
{: bash}

This will take a minute or so to run, it will vary depending on the random numbers. If we watch the output of `sacct` we should see 32 subjobs being created.

~~~
8324120.bat+      batch              hpcw0318         12  COMPLETED      0:0 
8324120.0          bash              hpcw0318          1  COMPLETED      0:0 
8324120.1          bash              hpcw0318          1  COMPLETED      0:0 
8324120.2          bash              hpcw0318          1  COMPLETED      0:0 
8324120.3          bash              hpcw0318          1  COMPLETED      0:0 
8324120.4          bash              hpcw0318          1  COMPLETED      0:0 
8324120.5          bash              hpcw0318          1  COMPLETED      0:0 
8324120.6          bash              hpcw0318          1  COMPLETED      0:0 
8324120.7          bash              hpcw0318          1  COMPLETED      0:0 
8324120.8          bash              hpcw0318          1  COMPLETED      0:0 
8324120.9          bash              hpcw0318          1  COMPLETED      0:0 
8324120.10         bash              hpcw0318          1  COMPLETED      0:0 
8324120.11         bash              hpcw0318          1  COMPLETED      0:0 
8324120.12         bash              hpcw0318          1  COMPLETED      0:0 
8324120.13         bash              hpcw0318          1  COMPLETED      0:0 
8324120.14         bash              hpcw0318          1  COMPLETED      0:0 
8324120.15         bash              hpcw0318          1  COMPLETED      0:0 
8324120.16         bash              hpcw0318          1  COMPLETED      0:0 
8324120.17         bash              hpcw0318          1  COMPLETED      0:0 
8324120.18         bash              hpcw0318          1  COMPLETED      0:0 
8324120.19         bash              hpcw0318          1  COMPLETED      0:0 
8324120.20         bash              hpcw0318          1  COMPLETED      0:0 
8324120.21         bash              hpcw0318          1  COMPLETED      0:0 
8324120.22         bash              hpcw0318          1  COMPLETED      0:0 
8324120.23         bash              hpcw0318          1  COMPLETED      0:0 
8324120.24         bash              hpcw0318          1  COMPLETED      0:0 
8324120.25         bash              hpcw0318          1  COMPLETED      0:0 
8324120.26         bash              hpcw0318          1  COMPLETED      0:0 
8324120.27         bash              hpcw0318          1  COMPLETED      0:0 
8324120.28         bash              hpcw0318          1  COMPLETED      0:0 
8324120.29         bash              hpcw0318          1  COMPLETED      0:0 
8324120.30         bash              hpcw0318          1  COMPLETED      0:0 
8324120.31         bash              hpcw0318          1  COMPLETED      0:0 
~~~
{: output}

The file `parallel_joblog` will contain a list of when each job ran and how long it took. 

~~~
Seq     Host    Starttime       JobRuntime      Send    Receive Exitval Signal  Command
1       :       1512606492.971      10.213      0       73      0       0       srun -n1 -N1 --exclusive /bin/bash ./runtask arg1:1
12      :       1512606495.364      10.102      0       75      0       0       srun -n1 -N1 --exclusive /bin/bash ./runtask arg1:12
10      :       1512606494.912      12.105      0       75      0       0       srun -n1 -N1 --exclusive /bin/bash ./runtask arg1:10
9       :       1512606494.707      13.099      0       73      0       0       srun -n1 -N1 --exclusive /bin/bash ./runtask arg1:9
4       :       1512606493.604      15.101      0       73      0       0       srun -n1 -N1 --exclusive /bin/bash ./runtask arg1:4
6       :       1512606494.041      15.101      0       73      0       0       srun -n1 -N1 --exclusive /bin/bash ./runtask arg1:6
5       :       1512606493.815      17.105      0       73      0       0       srun -n1 -N1 --exclusive /bin/bash ./runtask arg1:5
2       :       1512606493.178      19.098      0       73      0       0       srun -n1 -N1 --exclusive /bin/bash ./runtask arg1:2
7       :       1512606494.282      18.109      0       73      0       0       srun -n1 -N1 --exclusive /bin/bash ./runtask arg1:7
3       :       1512606493.392      19.105      0       73      0       0       srun -n1 -N1 --exclusive /bin/bash ./runtask arg1:3
8       :       1512606494.497      18.105      0       73      0       0       srun -n1 -N1 --exclusive /bin/bash ./runtask arg1:8
11      :       1512606495.151      19.109      0       75      0       0       srun -n1 -N1 --exclusive /bin/bash ./runtask arg1:11
13      :       1512606503.189      12.106      0       75      0       0       srun -n1 -N1 --exclusive /bin/bash ./runtask arg1:13
15      :       1512606507.021      10.107      0       75      0       0       srun -n1 -N1 --exclusive /bin/bash ./runtask arg1:15
17      :       1512606508.710      11.105      0       75      0       0       srun -n1 -N1 --exclusive /bin/bash ./runtask arg1:17
14      :       1512606505.471      15.111      0       75      0       0       srun -n1 -N1 --exclusive /bin/bash ./runtask arg1:14
21      :       1512606512.498      12.109      0       75      0       0       srun -n1 -N1 --exclusive /bin/bash ./runtask arg1:21
22      :       1512606512.713      12.103      0       75      0       0       srun -n1 -N1 --exclusive /bin/bash ./runtask arg1:22
19      :       1512606510.925      14.108      0       75      0       0       srun -n1 -N1 --exclusive /bin/bash ./runtask arg1:19
16      :       1512606507.811      18.111      0       75      0       0       srun -n1 -N1 --exclusive /bin/bash ./runtask arg1:16
23      :       1512606512.941      15.105      0       75      0       0       srun -n1 -N1 --exclusive /bin/bash ./runtask arg1:23
18      :       1512606509.147      19.108      0       75      0       0       srun -n1 -N1 --exclusive /bin/bash ./runtask arg1:18
24      :       1512606514.263      15.111      0       75      0       0       srun -n1 -N1 --exclusive /bin/bash ./runtask arg1:24
20      :       1512606512.280      17.105      0       75      0       0       srun -n1 -N1 --exclusive /bin/bash ./runtask arg1:20
25      :       1512606515.299      15.106      0       75      0       0       srun -n1 -N1 --exclusive /bin/bash ./runtask arg1:25
27      :       1512606519.820      14.111      0       75      0       0       srun -n1 -N1 --exclusive /bin/bash ./runtask arg1:27
28      :       1512606520.587      14.109      0       75      0       0       srun -n1 -N1 --exclusive /bin/bash ./runtask arg1:28
26      :       1512606517.132      18.102      0       75      0       0       srun -n1 -N1 --exclusive /bin/bash ./runtask arg1:26
30      :       1512606524.821      13.109      0       75      0       0       srun -n1 -N1 --exclusive /bin/bash ./runtask arg1:30
32      :       1512606525.927      15.106      0       75      0       0       srun -n1 -N1 --exclusive /bin/bash ./runtask arg1:32
29      :       1512606524.611      18.110      0       75      0       0       srun -n1 -N1 --exclusive /bin/bash ./runtask arg1:29
31      :       1512606525.037      19.107      0       75      0       0       srun -n1 -N1 --exclusive /bin/bash ./runtask arg1:31
~~~
{: output}

