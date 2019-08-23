---
title: "SCW Introduction"
author: "Colin Sauze"
teaching: 10
exercises: 0
questions:
 - "What does a High Performance Computing system consist of?"
keypoints: 
 - "A cluster is a group of computers connected together to act as one."
 - "Clusters are formed of nodes, each usually has several processors and 10s or hundreds of gigabytes of RAM."
 - "The Raspberry Pi is a simple single board computer with between one and four processor cores and half and four gigabytes of RAM."
objectives: 
 - "Understand what a cluster is"
---


# Prior Knowledge/Pre-requesites 

* Basic use of the Linux command line, as covered in the Software Carpentry Introduction to the Unix Shell Lesson.
* A laptop with WiFi access and an SSH client.

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

Each individual computer in a cluster is commonly referred to as a "node". Inside each node will be several processor chips that do the actual computation. Until around the mid 2000s most desktop/laptop computers had only a single processor, but since then most are multi-core meaning they effectively have multiple processors but all on one physical chip. A typical node in a cluster will have anything from 8 to 80 cores in total often across several physical processor chips. 

# Raspberry Pi

The Raspberry Pi is a low cost single board computer about the size of a credit card. The original version featured just a single core processor equivalent to a desktop computer from the late 1990s and 512 megabytes of RAM. The latest feature quad core processors and up to four gigabytes of RAM, its more equivalent to a desktop from the late 2000s. 

## Why build a cluster out Raspberry Pis?

* Its cheap
* It means we can teach without impacting on the real system
* Its much easier to run into and under resource limits
* We can see the real hardware instead of using something in a distant data centre





