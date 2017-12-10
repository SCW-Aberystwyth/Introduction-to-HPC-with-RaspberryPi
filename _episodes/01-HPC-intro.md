---
title: "SCW Introduction"
author: "Colin Sauze"
date: "December 2017"
teaching: 10
exercises: 0
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
* An account on HPC Wales.

# Cluster basics

Clusters, otherwise know as high-performance computing (HPC) or high-throughput computing systems, are large collections of relatively normal computers linked together through a "interconnect". 

These tools are becoming the <em>de facto</em> standard tools in most research disciplines today.

## What are some of reasons to use a cluster?

* Your computer does not have enough resources to run the desired analysis. *E.g.* memory, processors, disk space, or network bandwidth.
* You want to produce results faster than your computer can.
* You cannot install software in your computer. That is, the application does not have support for your operating system, conflicts with other existing applications, or softare licensing does not allow for installation on personal laptops.
* You want to leave something running while your computer would be turned off or doing something else.


## What does a cluster look like?

High Performance Computing most generally refers to the practice of aggregating computing power in a way that delivers much higher performance than one could get out of a typical desktop computer or workstation in order to solve large problems in science, engineering, or business.â€ --http://insidehpc.com/hpc-basic-training/what-is-hpc/

Clusters are simply a grouping of computers with the same components (RAM, disk, processors/cores, and networking cards) as those in your desktop or laptop, but with more umph! and are networked with high-speed interconnect that can be accessed (indirectly) through software, the scheduler, that manages simultaneous execution of jobs, or analyses, by multiple persons. 

![Overview of a compute cluster](../fig/cluster-generic.png)

The user accesses the compute cluster through one or more login nodes, and submits jobs to the scheduler, which will dispatch to and collect the completed work from the compute nodes. Frequently, clusters have shared disks, or filesystems, of various flavors where you can store your data, programs, and use for in-job execution (working or scratch areas)

## HPC Wales and Super Computing Wales

### HPC Wales

HPC Wales ran from 2010 to 2015 and provided clusters in Aberystwyth, Bangor, Cardiff, Glamorgan and Swansea. The Aberystwyth and Glamorgan systems have been decommissioned, but the Bangor, Cardiff and Swansea systems are still active.  

### SCW

Super Computing Wales (SCW) is a new project to replace HPC Wales. It started in 2017 and runs until 2020. It will include new systems in Cardiff and Swansea, but these haven't been installed yet. They are due in February 2018.


### How to get access?

Email support@hpcwales.co.uk with completed project and account forms. 
Everyone on this course should have a training account already, these are time limited. If you would like to use SCW for your research then you will have to apply.

#### Application Process

You will need to fill out two forms. One for your individual account and one for a project that you will be associated with. The account form gets you an account to login with, the project form is used to assess whether SCW/HPCW has enough resources for what you want. PhD students and RAs need to get your supervisor/PI to sign the form. Projects are assessed by the SCW management board. They are looking for two key targets:

  * Science Outputs (e.g. journal papers)
  * Bring in grant income, will this project help you to attract more funding.

If you are writing a grant application and intend to use SCW please mention it in the grant and let us know. There are project targets to bring in approx Â£8 million of funding, Aberystwyth's target is around £500k. This should be easily achievable, but bringing in far more will help us get follow on funding for SCW. 

