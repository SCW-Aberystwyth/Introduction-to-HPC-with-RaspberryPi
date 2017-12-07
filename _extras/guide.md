---
layout: page
title: "Instructor Notes"
permalink: /guide/
---

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

### Job Arrays
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
* Using sbatch
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

