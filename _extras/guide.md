---
layout: page
title: "Instructor Notes"
permalink: /guide/
---

# Intro


 * introduce everyone
 * get attendees to introduce themselves
 * etherpad link http://board.net/p/scwaber-2018-05-24

 
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

`ssh username@login.hpcwales.co.uk`

`hpcwhosts`

`sinfo`

`slurmtop`

## Exercises

* Logging in
* Run hpcwhosts
* Login to a host


# Moving Data
`sftp sftp.hpcwales.co.uk` 
Show filezilla

Home dirs are in `/hpcw/cf`, `/hpcw/sw` and `/hpcw/ba`

## Exercises

* run df -h
* run myquota
* Copy a file to bangor

# Running Jobs

## Interactive jobs
`salloc -n 1 --ntasks-per-node=1 ` 
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
`module load python/3.5.1`

## python modules

`module load http-proxy`
`pip3 install --user <mod>`
`pip3 install --user sklearn`

`from sklearn import datasets`
`digits = datasets.load_digits()`
`print(digits.data)`


## Exercises

* run a python script

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

`###`

`command1 &`

`command2 &`

`command3 &`

what if command1/2/3 take different amounts of time to run? 
We've got CPUs allocated but we aren't using them. Want to keep usage near to 100%

What if command4 needs to run after command1/2/3.

GNU parallel is a powerful program designed to run multiple jobs on a single node.
module called parallel contains it.

parallel.sh:

`#!/bin/bash --login`

`#SBATCH -n 12                     #Number of processors in our pool`

`#SBATCH -o output.%J              #Job output`

`#SBATCH -t 00:00:05               #Max wall time for entire job`

`module load parallel`

`# Define srun arguments:`

`srun="srun -n1 -N1 --exclusive" `

`# --exclusive     ensures srun uses distinct CPUs for each job step`

`# -N1 -n1         allocates a single core to each task`

`# Define parallel arguments:`

`parallel="parallel -N 1 --delay .2 -j $SLURM_NTASKS --joblog parallel_joblog --resume"`

`# -N 1              is number of arguments to pass to each job`

`# --delay .2        prevents overloading the controlling node on short jobs`

`# -j $SLURM_NTASKS  is the number of concurrent tasks parallel runs, so number of CPUs allocated`

`# --joblog name     parallel's log file of tasks it has run`

`# --resume          parallel can use a joblog and this to continue an interrupted run (job resubmitted)`

`# Run the tasks:`

`$parallel "$srun /bin/bash ./runtask.sh arg1:{1}" ::: {1..32}`

`# in this case, we are running a script named runtask, and passing it a single argument`

`# {1} is the first argument`

`# parallel uses ::: to separate options. Here {1..32} is a shell expansion defining the values for`

`#    the first argument, but could be any shell command`

`#`

`# so parallel will run the runtask script for the numbers 1 through 32, with a max of 12 running `

`#    at any one time`

`#`

`# as an example, the first job will be run like this:`

`#    srun -N1 -n1 --exclusive ./runtask arg1:1`

task.sh, the script which will actually be run

`#!/bin/bash`

`# this script echoes some useful output so we can see what parallel and srun are doing`

`sleepsecs=$[($RANDOM % 10) + 10]s`

`# $1 is arg1:{1} from parallel, it will be a number between 0 and 32`

`# $PARALLEL_SEQ is a special variable from parallel. It the actual sequence number of the job regardless of the arguments given`

`# We output the sleep time, hostname, and date for more info&gt;`

`echo task $1 seq:$PARALLEL_SEQ sleep:$sleepsecs host:$(hostname) date:$(date)`

`# sleep a random amount of time`

`sleep $sleepsecs`

submit it:

`sbatch parallel.sh`

sacct will show 32 subjobs. 

parallel_joblog shows how long each took to run.

