---
title: "SCW Introduction"
author: "Colin Sauze"
teaching: 10
exercises: 0
questions:
 - "What is Super Computing Wales and how do I get access to it?"
keypoints: 
 - "A cluster is a group of computers connected together to act as one."
 - "Clusters are formed of nodes, each usually has several processors and 10s or hundreds of gigabytes of RAM."
 - "HPCW/SCW have clusters for researchers at Welsh universities to use"
objectives: 
 - "Understand what a cluster is"
 - "Understand the background to the HPC Wales and Super Computing Wales projects"
---


# Prior Knowledge/Pre-requesites 

* Basic use of the Linux command line, as covered in the Software Carpentry Introduction to the Unix Shell Lesson.
* An account on Super Computing Wales.

# Cluster basics

Clusters, otherwise know as high-performance computing (HPC) or high-throughput computing systems, are large collections of relatively normal computers linked together through a "interconnect". 

These tools are becoming the <em>de facto</em> standard tools in most research disciplines today.

## What are some of reasons to use a cluster?

* Your computer does not have enough resources to run the desired analysis. *E.g.* memory, processors, disk space, or network bandwidth.
* You want to produce results faster than your computer can.
* You cannot install software in your computer. That is, the application does not have support for your operating system, conflicts with other existing applications, or softare licensing does not allow for installation on personal laptops.
* You want to leave something running while your computer would be turned off or doing something else.


## What does a cluster look like?

High Performance Computing most generally refers to the practice of aggregating computing power in a way that delivers much higher performance than one could get out of a typical desktop computer or workstation in order to solve large problems in science, engineering, or business. --http://insidehpc.com/hpc-basic-training/what-is-hpc/

Clusters are simply a grouping of computers with the same components (RAM, disk, processors/cores, and networking cards) as those in your desktop or laptop, but with more umph! and are networked with high-speed interconnect that can be accessed (indirectly) through software, the scheduler, that manages simultaneous execution of jobs, or analyses, by multiple persons. 

![Overview of a compute cluster](../fig/cluster-generic.png)

The user accesses the compute cluster through one or more login nodes, and submits jobs to the scheduler, which will dispatch to and collect the completed work from the compute nodes. Frequently, clusters have shared disks, or filesystems, of various flavors where you can store your data, programs, and use for in-job execution (working or scratch areas)

## Nodes and Cores

Each individual computer in a cluster is commonly referred to as a "node". Inside each node will be several processor chips that do the actual computation. Until around the mid 2000s most desktop/laptop computers had only a single processor, but since then most are multi-core meaning they effectively have multiple processors but all on one physical chip. A typical node in a cluster will have anything from 8 to 40 cores in total often across several physical processor chips. 

## HPC Wales and Super Computing Wales

### HPC Wales

HPC Wales ran from 2010 to 2015 and provided clusters in Aberystwyth, Bangor, Cardiff, Glamorgan and Swansea. The final systems are being shutdown in late 2018, all users should now use Super Computing Wales.

### SCW

Super Computing Wales (SCW) is a new project to replace HPC Wales involving Aberystwyth, Bangor, Cardiff and Swansea universities. It started in 2015 and runs until 2020. It will include new systems in Cardiff (known as Hawk) and Swansea (known as Sunbird). 

## Super Computing Wales Research Software Engineers

Each university is employing research software engineers who will work with researchers to:

* Convert existing software to run on the HPC system
* Optimise code to run more efficiently on HPC systems
* Write new software
* Help with training, on-boarding and project development


### How to get access?

Complete a project application form via the (currently unavilable) web portal.
Everyone on this course should have a training account already, these are time limited. If you would like to use SCW for your research then you will have to apply.

#### Application Process

You will need to fill out two online forms. One for your individual account and one for a project that you will be associated with. The account form gets you an account to login with, the project form is used to assess whether SCW has enough resources for what you want. PhD students and RAs need to get your supervisor/PI to approve their projects. Projects are assessed by SCW. They are looking for two key targets:

  * Grant income that can be attributed to Super Computing Wales.
  * Science Outputs (e.g. journal papers)
  
At this stage you do NOT need to pay any money to SCW, simply attribute that the grant funding required access to the system. Funding which attributes other projects funded by the Welsh European Funding Office (WEFO) cannot be counted towards SCW. 

If you are writing a grant application and intend to use SCW please mention it in the grant and let us know. There are project targets to bring in approx £8 million of funding, Aberystwyth's target is around £800k. This should be easily achievable, but bringing in far more will help us get follow on funding for SCW. 

