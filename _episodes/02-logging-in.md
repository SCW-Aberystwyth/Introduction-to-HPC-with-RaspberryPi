---
title: "Logging in to SCW"
author: "Colin Sauze"
teaching: 20
exercises: 15
questions:
 - "How can do I login to SCW?"
objectives: 
 - "Understand how to login to SCW"
 - "Understand the difference between the login node and each cluster's head node."
keypoints:
 - "ssh login.hpcwales.co.uk for the login node, from there connect to the cluster of your choice"
 - "hpcwhosts command shows a list of clusters"
---



# Logging in 

Your username is usually `firstname.surname`. You should have been emailed details of your login prior to this workshop.

~~~
$ ssh username@login.hpcwales.co.uk
~~~
{: .bash}

Windows users should use PuTTY and enter login.hpcwales.co.uk in the hostname box. 

## Change your password

If you haven't already changed your password from the one that was emailed to you, do so now by running the ```passwd``` command. Passwords need to contain some numbers, letters and punctuation characters. If you forget your password email support@hpcwales.co.uk to reset it.


## What's available?

### HPC Wales

The `hpcwhosts` command will list the available clusters. 

~~~
$ hpcwhosts
~~~
{: .bash}

~~~
HPC Wales Clusters Available

Phase    System Location & Type             Login Node(s)
------------------------------------------------------------------
1        Cardiff High Throughput            cwl001   cwl002   cwl003
1        Bangor Medium Processing           bwl001   bwl002
2        Swansea Capability/Capacity/GPU    ssl001   ssl002   ssl003
2        Cardiff Capacity/GPU               csl001   csl002
~~~
{: .output}


|Cluster|Number of Nodes|Cores per node|Architecture|RAM|Other|
|---|---|---|---|---|---|
|Cardiff High Throughput|~~162~~ 54|12|Westmere|36GB||
|Cardiff High Throughput|4|2|Nehalem|128GB||
|Cardiff High Throughput|1|8|Nehalem|512GB||
|Cardiff Capacity|~~384~~ 116|16|Sandy Bridge|64GB||
|Cardiff GPU|~~16~~ 4|16|Sandy Bridge|64GB|Nvidia Tesla M GPU|
|Swansea Capability|16|16|Sandy Bridge|128GB||
|Swansea Capability|240|16|Sandy Bridge|64GB||
|Swansea Capacity|128|16|Sandy Bridge|64GB||
|Swansea GPU|16|16|Sandy Bridge|64GB|Nvidia Tesla M2090 (512 core, 6GB RAM)|
|Bangor|54|12|Westmere|36GB||

### Super Computing Wales

These figures may still be subject to some change and might have been sourced from out of date documents. 

|Cluster|Number of Nodes|Cores per node|Architecture|RAM|Other|
|---|---|---|---|---|---|
|Swansea|118|20|Skylake|384GB||
|Swansea GPU|4|20|Skylake|384GB|Nvidia V100 (5120 core, 16GB RAM)|
|Swansea Data Lake|?|?||?|?|?|Installed with Swansea system|
|Cardiff MPI|136|20|Sylake|196GB||
|Cardiff HTC|25|20|Sylake|196GB||
|Cardiff High Memory|26|20|Sylake|382GB||
|Cardiff GPU|13|20?|Skylake|?|Nvidia P100 (3584 core, 16GB RAM)|
|Cardiff Data Lake|2|22|Skylake|512GB|Will be installed later|

Aberystwyth users are expected to use the Swansea system and will need to make a case for why they would need to use the Cardiff system. Bangor users are expected to use Cardiff.

SCW is still in the process of being installed. A single SkyLake core is approximately double the speed of a Sandybridge core. 

### Slurm

Slurm is the management software used on HPC Wales. It lets you submit (and monitor or cancel) jobs to the cluster and chooses where to run them. 

Other clusters might run different job management software such as LSF, Sun Grid Engine or Condor, although they all operate along similar principles.


### How busy is the cluster?

The ```sinfo``` command tells us the state of the cluster. It lets us know what nodes are available, how busy they are and what state they are in. 

Clusters are sometimes divided up into partitions. This might separate some nodes which are different to the others (e.g. they have more memory, GPUs or different processors). 

~~~
PARTITION AVAIL  TIMELIMIT  NODES  STATE NODELIST
work*        up   infinite      2 drain* bwc[022,052]
work*        up   infinite      1  down* bwc016
work*        up   infinite     13    mix bwc[001-002,010-012,031-036,050-051]
work*        up   infinite     38  alloc bwc[003-009,013-015,017-021,023-030,037-049,053-054]
long         up   infinite      2 drain* bwc[022,052]
long         up   infinite      1  down* bwc016
long         up   infinite     13    mix bwc[001-002,010-012,031-036,050-051]
long         up   infinite     38  alloc bwc[003-009,013-015,017-021,023-030,037-049,053-054]
~~~
{: .output}

 * work* means this is the default partition. 
 * AVAIL tells us if the partition is available.
 * TIMELIMIT tells us if there's a time limit for jobs
 * NODES is the number of nodes in the this partition.
 * STATE, drain means the node will become unavailable once the current job ends. down is off, allow is allocated and mix is ...



# Exercises

> ## Logging into HPC Wales
> 1. Login to login.hpcwales.co.uk using your SSH client. Your username is usually firstname.surname and has been emailed to you.
> 2. Run the `hpcwhosts` and pick a system to login to.
> 3. Login to that host by running `ssh <hostname>`
> 4. Run the `sinfo` command to see how busy things are.
> 5. Try `sinfo --long`, what extra information does this give?
{: .challenge}

