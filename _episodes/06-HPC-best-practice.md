---
title: "HPC Best Practice"
author: "Colin Sauze"
questions:
 - "What are the best practices for using an HPC system?"
objectives: 
 - "Understand HPC best practice"
---


# HPC Best Practice

* Don't run jobs on login/head nodes
* Don't run too many jobs at once. SCW has a limit of 26 nodes/1040 cores
* Don't use all the disk space on scratch. Don't leave old files on there.
* Don't create/leave excessive numbers of files on scratch. Large file counts can cause problems for the filesystem.
* Try to use all the cores on a node, especially if you take the node exclusively. Sometimes with large memory jobs this isn't possible.
* Make jobs that last at least a few minutes, lots of small jobs creates excess load on the scheduler. Use something like GNU Parallel to make each Slurm job do several things.


## Best Practices

Again, working on a cluster is working in a big sandbox, with people of all ages and skills. So it is
important to work carefully and be considerate. Please visit our list of Common Pitfalls and 
Fair Use/Responsibilities pages so that you'll be a good member of the community...

[Common Pitfalls](https://rc.fas.harvard.edu/resources/documentation/common-odyssey-pitfalls/)
[Fair Use/Responsibilities:](https://rc.fas.harvard.edu/resources/responsibilities/)

