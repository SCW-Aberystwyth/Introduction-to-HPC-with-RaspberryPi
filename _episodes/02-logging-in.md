---
title: "Logging in to the cluster"
author: "Colin Sauze"
teaching: 20
exercises: 15
questions:
 - "How can do I login to the cluster?"
objectives: 
 - "Understand how to login to the cluster"
 - "Understand the difference between the login node and compute nodes."
keypoints:
 - "ssh lets us login to a remote computer system"
 - "sinfo shows partitions and how busy they are."
---



# Logging in 

Your username is your first name and your password is your email that you registered for the workshop with. 

Connect your laptop to the WiFi network called "TweetyPi", the password is "Raspberries". The address of the login node is 10.0.0.10.

~~~
$ ssh username@10.0.0.10
~~~
{: .bash}

Windows PuTTY users should enter 10.0.0.10 in the hostname box. 

This will connect you to the login node.


## What's available?

### Slurm

Slurm is the management software used on many real HPC systems including Super Computing Wales. It lets you submit (and monitor or cancel) jobs to the cluster and chooses where to run them. All the commands you are using in this workshop should work on any HPC system running Slurm.

Other clusters might run different job management software such as LSF, Sun Grid Engine or Condor, although they all operate along similar principles.


### How busy is the cluster?

The ```sinfo``` command tells us the state of the cluster. It lets us know what nodes are available, how busy they are and what state they are in. 

Clusters are sometimes divided up into partitions. This might separate some nodes which are different to the others (e.g. they have more memory, GPUs or different processors). 

~~~
PARTITION AVAIL  TIMELIMIT  NODES  STATE NODELIST
compute*     up   infinite     10   idle worker[00-09]
~~~
{: .output}

 * compute* means this is the default partition. 
 * AVAIL tells us if the partition is available.
 * TIMELIMIT tells us if there's a time limit for jobs
 * NODES is the number of nodes in the this partition.
 * STATE, drain means the node will become unavailable once the current job ends. down is off, allow is allocated and idle is unused.



# Exercises

> ## Logging into the Cluster
> 1. Connect to the TweetyPi network, the password is Raspberries
> 2. Login to 10.0.0.10, the username is your first name and password is your email address. 
> 3. Change your password with the passwd command.
> 4. Run the `sinfo` command to see how busy things are.
> 5. Try `sinfo --long`, what extra information does this give?
{: .challenge}

