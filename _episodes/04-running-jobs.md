---
title: "Running Jobs with Slurm"
author: "Colin Sauze"
teaching: 25
exercises: 30
questions: 
 - "How do I run a job with the Slurm scheduler?"
objectives: 
 - "Understand how to submit an interactive job using Slurm"
 - "Understand how to submit a batch job using Slurm"
 - "Understand how to set the parameters for your Slurm job"
 - "Understand the concept of job arrays"
keypoints:
 - "Interactive jobs let you test out the behaviour of a command, but aren't pratical for running lots of jobs"
 - "Batch jobs are suited for submitting a job to run without user interaction."
 - "Job arrays are useful to submit lots of jobs."
 - "Slurm lets you set parameters about how many processors or nodes are allocated, how much memory or how long the job can run."
---


# Working with the scheduler

The scheduler is responsible for listening to your job requests, then finding the proper compute node that meets your job's resource requirements -- RAM, number of cores, time, etc --. It dispatches the job to a compute node, collects info about the completed work, and stores information about your job. If you've asked it to do so, it will even notify you about the status of your job (e.g. begin, end, fail, etc).


## Running interactive jobs

There are two ways to run jobs on a cluster. One, usually done at the start, is to get an
interactive/foreground session on a compute node. This will give you a command prompt on a compute node and let you run the commands of your choice there. 

If you want to experiment with some code and test it you should run it this way.

** Don't run jobs on the login nodes **


To get an interactive session, you first need to issue a `salloc` command to reserve some resources. 


~~~
salloc -n 1 
~~~
{: .bash}

The salloc command will respond now with a job ID number. 

~~~
salloc: Granted job allocation 21712
salloc: Waiting for resource configuration
salloc: Nodes scs0018 are ready for job
~~~
{: .output}

>


We have now allocated ourselves a host to run a program on. The `-n 1` tells slurm how many copies of the task we will be running. The `--ntasks-per-node=1` tells Slurm that we will just be running one task for every node we are allocated. We could increase either of these numbers if we want to run multiple copies of a task and if we want to run more than one copy per node. 

The `--account` option tells Slurm which project to account your usage against, if you are only a member of one project then this will default to that project. If you're a member of multiple projects then it will default to the first one. The accounting information is used to measure what resources a project has consumed and to prioritise its use, so its important to choose the right project. 

To ensure nodes are available for this training workshop a reservation may have been made to prevent anyone else using a few nodes. In order to make use of these you must use the `--reservation` option too, if you don't then you'll have to wait in the same queue as everyone else. 

To actually run a command we now need to issue the `srun` command. This also takes a `-n` parameter to tell Slurm how many copies of the job to run and it takes the name of the program to run. To run a job interactively we need another argument `--pty`. 

~~~
srun --pty /bin/bash
~~~
{: .bash}


If you run command above you will see the hostname in the prompt change to the name of the compute node that slurm has allocated to you. In the example below the compute node is called `scs0018`. 
 
~~~
[s.jane.doe@sl1 ~]$ srun --pty /bin/bash
[s.jane.doe@scs0018 ~]$ 
~~~
{: .output}

We are now logged into a compute node and can run any commands we wish and these will run on the compute node instead of the login node. You can also confirm the name of the host that you are connected to by running the `hostname` command.

~~~
hostname
~~~
{: .bash}

~~~
scs0018
~~~
{: .output}


Once we are done working with the compute node we need to disconnect from it. The `exit` command will exit the bash program on the compute node causing us to disconnect. After this command is issued the hostname prompt should change back to the login node's name (e.g. sl1 or cl1). 

~~~
[s.jane.doe@scs0018  ~]$ exit
exit
[s.jane.doe@sl1 ~]$ 
~~~
{: .output}

At this point we still hold an allocation for a node and could run another job if we wish. We can confirm this by examining the queue of our jobs with the `squeue` command.

~~~
squeue
~~~
{: .bash}

~~~
             JOBID PARTITION     NAME     USER ST       TIME  NODES NODELIST(REASON)
           21712   compute     bash s.jane.doe  R       3:58      1 scs0018
~~~
{: .output}

To relinquish the node allocation we need to issue another exit command. 

~~~
[s.jane.doe@sl1 ~]$ exit
~~~
{: .bash}

This will display a message that the job allocation is being relinquished and show us the same job ID number again.

~~~
exit
salloc: Relinquishing job allocation 21712
~~~
{: .output}

At this point our job is complete and we no longer hold any allocations. We can confirm this again with the `squeue` command.

~~~
[s.jane.doe@sl1 ~]$ squeue
~~~
{: .bash}

~~~
             JOBID PARTITION     NAME     USER ST       TIME  NODES NODELIST(REASON)
~~~
{: .output}




## Running batch jobs

For most situations we won't want to run a job interactively, instead we will want to submit it to the cluster have it do its work and return any output files to us. We might submit many copies of the same job with different parameters in this way. This method of working is known as batch processing. To do this we must first write some details about our job into a script file. Use `nano` (or your favourite command line text editor) and create a file containing the following:

~~~
nano batchjob.sh
~~~
{: .bash}

~~~
#!/bin/bash --login
###
#job name
#SBATCH --job-name=hostname
#job stdout file
#SBATCH --output=hostname.out.%J
#job stderr file
#SBATCH --error=hostname.err.%J
#maximum job time in D-HH:MM
#SBATCH --time=0-00:01
#SBATCH --ntasks=1
###

/bin/hostname

~~~
{: .bash}

This is actually a bash script file containing all the commands that will be run. Lines beginning with a `#` are comments which bash will ignore. However lines that begin `#SBATCH` are instructions for the `sbatch` program. The first of these (`#SBATCH --job-name=hostname`) tells sbatch the name of the job, in this case we will call the job hostname. The `--output` line tells sbatch where output from the program should be sent, the `%J` in its name means the job number. The same applies for the `--error` line, except here it is for error messages that the program might generate, in most cases this file will be blank. The `--time` line limits how long the job can run for, this is specified in days, hours and minutes. The `--mem-per-cpu` tells Slurm how much memory to allow the job to use on each CPU it runs on, if the job exceeds this limit Slurm will automatically stop it. You can set this to zero for no limits. However by putting in a sensible number you can help allow other jobs to run on the same node. The final line specifies the actual commands which will be executed, in this case its the `hostname` command which will tell us the name of the compute node which ran our job.

Lets go ahead and submit this job with the `sbatch` command.

~~~
[s.jane.doe@sl1 ~]$ sbatch batchjob.sh
~~~
{: .bash}


sbatch will respond with the number of the job.

~~~
Submitted batch job 3739464
~~~
{: .output}

Our job should only take a couple of seconds to run, but if we are fast we might see it in the `squeue` list.

~~~
[s.jane.doe@sl1 ~]$ squeue
~~~
{: .bash}

~~~
             JOBID PARTITION     NAME     USER ST       TIME  NODES NODELIST(REASON)
           3739464      work hostname jane.doe  R       0:01      1 scs0018
~~~
{: .output}

Once the job is completed two new files should be created, one called `hostname.out.3739464` and one called `hostname.err.3739464`. The `.out` file is the output from the command we ran and the `.err` is the errors from that command. Your job files will have different names as they will contain the job ID you were allocated and not `3739464`. Lets go ahead and look at the `.out` file:

~~~
[s.jane.doe@sl1 ~]$ cat hostname.out.373464
~~~
{: .bash}

~~~
scs0018
~~~
{: .output}

If we check the `.err` file it should be blank:

~~~
[s.jane.doe@sl1 ~]$ cat hostname.err.373464
~~~
{: .bash}

~~~
~~~
{: .output}


### Over-riding the sbatch options from the command line

As well as specifying options to sbatch in the batch file, they can specified on the command line too.
Lets edit our batch file to run the command `/bin/sleep 70` before `/bin/hostname`, this will cause it to wait for 70 seconds before exiting. As our job has a one minute limit this should fail and the hostname output will never happen.


~~~
[s.jane.doe@sl1 ~]$ nano batchjob.sh
~~~
{: .bash}


Edit the script to have the command `/bin/sleep 70` before the `hostname` command. 
~~~
#!/bin/bash --login
###
#job name
#SBATCH --job-name=hostname
#job stdout file
#SBATCH --output=hostname.out.%J
#job stderr file
#SBATCH --error=hostname.err.%J
#maximum job time in D-HH:MM
#SBATCH --time=0-00:01
#SBATCH --ntasks=1
#SBATCH --nodes=1
###

/bin/sleep 70
/bin/hostname
~~~
{: .bash}


Now lets resubmit the job.

~~~
[s.jane.doe@sl1 ~]$  sbatch batchjob.sh
~~~
{: .bash}

~~~
Submitted batch job 3739465
~~~
{: .output}

After approximately one minute the job will disappear from the `squeue` output, but this time the `.out` file should be empty and the `.err` file will contain an error message saying the job was cancelled:

~~~
[s.jane.doe@sl1 ~]$  cat hostname.err.3739465
~~~
{: .bash}


~~~
slurmstepd: error: *** JOB 3739465 ON scs0018 CANCELLED AT 2017-12-06T16:45:38 DUE TO TIME LIMIT ***
~~~
{: .output}

~~~
[s.jane.doe@sl1 ~]$ cat hostname.out.3739465
~~~
{: .bash}


~~~
~~~
{: .output}



Now lets override the time limit by giving the parameter `--time 0-0:2` to sbatch, this will set the time limit to two minutes and the job should complete.

~~~
[s.jane.doe@sl1 ~]$ sbatch --time 0-0:2 batchjob.sh
~~~
{: .bash}

~~~
 Submitted batch job 3739466
~~~
{: .output}

After approximately 70 seconds the job will disappear from the squeue list and this we should have nothing in the `.err` file and a hostname in the `.out` file. 

~~~
[s.jane.doe@sl1 ~]$ cat hostname.err.3739466
~~~
{: .bash}

~~~
~~~
{: .output}


~~~
[s.jane.doe@sl1 ~]$ cat hostname.out.3739466
~~~
{: .bash}

~~~
scs0018
~~~
{: .output}


### Cancelling jobs

The `scancel` command can be used to cancel a job after its submitted. Lets go ahead and resubmit the job we just used.

~~~
[s.jane.doe@sl1 ~]$  sbatch batchjob.sh
~~~
{: .bash}

~~~
Submitted batch job 3739467
~~~
{: .output}


Now (within 60 seconds) lets cancel the job.


~~~
[s.jane.doe@sl1 ~]$  scancel 3739467
~~~
{: .bash}

This will cancel the job, `squeue` will now show no record of it and there won't be a `.out` or `.err` file for it. 


> ## Using the `sbatch` command. 
> 1. Write a submission script to run the hostname command on one node, with one core and a maximum run time of one minute. Have it save its output to hostname.out.%J and errors to hostname.err.%J.
> 2. Run your script using `sbatch`
> 3. Examine the output file, which host did it run on?
> 4. Try running it again, did your command run on the same host? 
> 5. Now add the command `/bin/sleep 120` before the line running hostname in the script. Run the job again and examine the output of `squeue` as it runs. How many seconds does the job run for before it ends? Hint: the command `watch -n 1 squeue` will run squeue every second and show you the output. Press CTRL+C to stop it. 
> 6. What is in the .err file, why did you script exit? Hint: if it wasn't due to the time expiring try altering another parameter so it is due a time expiration. 
{: .challenge}

## Running multiple copies of a job with Srun

So far we've only run a single copy of a program. Often we'll need to run multiple copies of something. To do this we can combine the `sbatch` and `srun` commands. Instead of just placing the command at the end of the script we'll `srun` the command. 
This will allow multiple copies of the command to run. In the example below two copies of the hostname command are run on two different nodes. 

~~~
#!/bin/bash --login
###
#job name
#SBATCH --job-name=hostname
#job stdout file
#SBATCH --output=hostname.out.%J
#job stderr file
#SBATCH --error=hostname.err.%J
#maximum job time in D-HH:MM
#SBATCH --time=0-00:01
#SBATCH --ntasks=2
#SBATCH --nodes=2
###

srun /bin/hostname
~~~
{: .bash}

Save this as job.sh and run it with sbatch

~~~
[s.jane.doe@sl1 ~]$ sbatch job.sh
~~~
{: .bash}

The output will now go into hostname.out.jobnumber and should contain two different hostnames. 


## Job Arrays

Job Arrays are another method for running multiple copies of the same job. The `--array` parameter to sbatch allows us to make use of this feature.

~~~
[s.jane.doe@sl1 ~]$ sbatch --array=0-2 batchjob.sh
~~~
{: .bash}

The above command will submit **three** copies of the batchjob.sh command. 

~~~
[s.jane.doe@sl1 ~]$ squeue 
             JOBID PARTITION     NAME     USER   ST       TIME  NODES NODELIST(REASON)
         3739590_0   compute hostname s.jane.doe  R       0:01      1 scs0018
         3739590_1   compute hostname s.jane.doe  R       0:01      1 scs0018
         3739590_2   compute hostname s.jane.doe  R       0:01      1 scs0096
~~~
{: .bash}

Running `squeue` as this is happening will show three distinct jobs, each with an _ followed by a number on the end of their job ID. When the jobs are complete there will be three output and three err files all with the job ID and the job array number.

~~~
[s.jane.doe@sl1 ~]$ ls -rt | tail -6
hostname.out.3739592.scs0018
hostname.out.3739591.scs0018
hostname.out.3739590.scs0096
hostname.err.3739590.scs0096
hostname.err.3739592.scs0018
hostname.err.3739591.scs0018
~~~
{: .bash}

Its possible for programs to get hold of their array number from the `$SLURM_ARRAY_TASK_ID` environment variable. If we add the command `echo $SLURM_ARRAY_TASK_ID` to our batch script then it will be possible to see this in the output file. 


> ## Using job arrays
> 1. Add the following to the end of your job script
> `echo $SLURM_ARRAY_TASK_ID`
> 2. Submit the script with the `sbatch --array=0-1` command. 
> 3. When the job completes look at the outut file. What does the last line contain?
> 4. Try resubmitting with different array numbers, for example `10-11`. Be careful not to create too many jobs.
> 5. What use is it for a job to know its array number? What might it do with that information?
> 6. Try looking at the variables `$SLURM_JOB_ID` and `$SLURM_ARRAY_JOB_ID` what do these contain?
>
> > ## Solution
> > 3. The last line of the output files should contain 0 and 1
> > 4. If you set the array IDs to 10 and 11 thne the output should contain 10 and 11.
> > 5. Its useful to act as a parameter for partitioning datasets that each job will process a subpart of.
> > 6. The job ID and the parent ID of the array job. The parent ID is usually one less than ID of the first array job. 
> {: .solution}
{: .challenge}


## Choosing the proper resources for your job

When you submit a job, you are requesting resources from the scheduler to run your job. These are:
* time
* memory
* Number of cores (CPUs)
* Number of nodes
* (sort of) queue or group of machines to use

Choosing resources is like playing a game with the scheduler: You want to request enough to get your job completed without failure, But request too much: your job is "bigger" and thus harder to schedule. Request too little: if your job goes over that requested, it is killed. So you want to get it just right, and pad a little for wiggle room.

Another way to think of 'reserving' a compute node for you job is like making a reservation at a restaurant:
* if you bring more guests to your dinner, there won't be room at the restaurant, but the wait staff may try to fit them in. If so, things will be more crowded and the kitchen (and the whole restaurant) may slow down dramatically
* if you bring fewer guests and don't notify the staff in advance, the extra seats are wasted; no one else can take the empty places, and the restaurant may lose money.

Never use a piece of software for the first time without looking to see what command-line options are available and what default parameters are being used
	-- acgt.me · by Keith Bradnam
	


# More information about Slurm 

* [Super Computing Wales Documentation](http://portal.supercomputing.wales)
* [Harvard University's list of common Slurm commands](https://rc.fas.harvard.edu/resources/documentation/convenient-slurm-commands/)
* [For those coming from another cluster/scheduler, check out Slurm's scheduler Rosetta stone](http://slurm.schedmd.com/rosetta.pdf)
