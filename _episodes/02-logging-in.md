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

Your username is your institutional ID prefixed by 'a' for Aberystwyth users, 'b' for Bangor users, 'c' for Cardiff users and 's' for Swansea users. External collaborators will have a username beginning with a 'x'. 

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
{: .bash}

Windows PuTTY users should enter hawklogin.cf.ac.uk in the hostname box. 


## What's available?

### Super Computing Wales

These figures may still be subject to some change and might have been sourced from out of date documents. 

|Partition|Number of Nodes|Cores per node|RAM|Other|
|-------|----|----|------|----|------|
|Swansea Compute|122|40|376GB||
|Swansea GPU|4|40|376GB|Nvidia V100 (5120 core, 16GB RAM)|
|Swansea Data Lake|1|72||1500GB|Installed with Swansea system, not available for general use yet. Intended for Hadoop and Elastic Stack users.|


|Cluster|Number of Nodes|Cores per node|RAM|Other|
|-------|----|----|------|----|------|
|Cardiff Compute|136|40|196GB||
|Cardiff HTC|26|40|196GB||
|Cardiff High Memory|26|40|376GB||
|Cardiff GPU|13|40|376GB|2x Nvidia P100 (3584 core, 16GB RAM)|
|Cardiff Dev|2|40|196GB||
|Cardiff Data Lake|2|?|Skylake|?|Will be installed later. Intended for Hadoop and Elastic Stack users.|

Aberystwyth users are expected to use the Swansea system and will need to make a case for why they would need to use the Cardiff system. Bangor users are expected to use Cardiff.


### Slurm

Slurm is the management software used on Super Computing Wales. It lets you submit (and monitor or cancel) jobs to the cluster and chooses where to run them. 

Other clusters might run different job management software such as LSF, Sun Grid Engine or Condor, although they all operate along similar principles.


### How busy is the cluster?

The ```sinfo``` command tells us the state of the cluster. It lets us know what nodes are available, how busy they are and what state they are in. 

Clusters are sometimes divided up into partitions. This might separate some nodes which are different to the others (e.g. they have more memory, GPUs or different processors). 

~~~
PARTITION AVAIL  TIMELIMIT  NODES  STATE NODELIST
compute*     up 3-00:00:00      1   fail scs0042
compute*     up 3-00:00:00      1 drain* scs0004
compute*     up 3-00:00:00      2    mix scs[0018,0065]
compute*     up 3-00:00:00     86  alloc scs[0001-0003,0005-0017,0019-0035,0043-0046,0049-0064,0066-0072,0097-0122]
compute*     up 3-00:00:00     32   idle scs[0036-0041,0047-0048,0073-0096]
gpu          up 2-00:00:00      4   idle scs[2001-2004]
~~~
{: .output}

 * compute* means this is the default partition. 
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

