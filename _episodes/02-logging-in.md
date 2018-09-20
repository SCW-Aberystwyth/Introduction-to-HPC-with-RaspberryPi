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

Your username is your institutional ID prefixed by 'a' for Aberystwyth users, 'b' for Bangor users, 'c' for Cardiff users and 's' for Swansea users.

Aberystwyth and Swansea users should login to the Swansea Sunbird system by typing:

~~~
$ ssh username@sunbird.swansea.ac.uk
~~~
{: .bash}

Windows users should use PuTTY and enter sunbird.swansea.ac.uk in the hostname box. 


Bangor and Cariff Users should login to the Cardiff Hawk system by typing:

~~~
$ ssh username@hawklogin.cf.ac.uk
~~~

Windows PuTTY users should enter hawklogin.cf.ac.uk in the hostname box. 


## Change your password

If you haven't already changed your password from the one that was emailed to you, do so now by running the ```passwd``` command. Passwords need to contain some numbers, letters and punctuation characters. If you forget your password email support@hpcwales.co.uk to reset it.


## What's available?

### Super Computing Wales

These figures may still be subject to some change and might have been sourced from out of date documents. 

|Partition|Number of Nodes|Cores per node|Architecture|RAM|Other|
|-------|----|----|------|----|------|
|Swansea Compute|122|40|Skylake|376GB||
|Swansea GPU|4|40|Skylake|376GB|Nvidia V100 (5120 core, 16GB RAM)|
|Swansea Data Lake|?|?||?|?|?|Installed with Swansea system|


|Cluster|Number of Nodes|Cores per node|Architecture|RAM|Other|
|-------|----|----|------|----|------|
|Cardiff Compute|136|40|Sylake|196GB||
|Cardiff HTC|26|40|Sylake|196GB||
|Cardiff High Memory|26|40|Sylake|376GB||
|Cardiff GPU|13|40|Skylake|376GB|2x Nvidia P100 (3584 core, 16GB RAM)|
|Cardiff Dev|2|40|Skylake|
|Cardiff Data Lake|2|22|Skylake|512GB|Will be installed later|

Aberystwyth users are expected to use the Swansea system and will need to make a case for why they would need to use the Cardiff system. Bangor users are expected to use Cardiff.


### Slurm

Slurm is the management software used on Super Computing Wales. It lets you submit (and monitor or cancel) jobs to the cluster and chooses where to run them. 

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

> ## Logging into Super Computing Wales
> 1. In your web browser go to https://my.supercomputing.wales and login with your university username and password. 
> 2. Click on "Reset SCW Password" and choose a new password for logging into the HPC. Your username is displayed in the "Account summary" box on the main page. Its usually a/b/c/s. and your normal university login.
> 3. Login to sunbird.swansea.ac.uk or hawklogin.cf.ac.uk using your SSH client.
> 4. Run the `sinfo` command to see how busy things are.
> 5. Try `sinfo --long`, what extra information does this give?
{: .challenge}

