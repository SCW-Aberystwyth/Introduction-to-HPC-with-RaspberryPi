---
title: Distributing computations among computers with MPI
teaching: 45
exercises: 10
questions:
- "What issued the message passing interface (MPI)?"
- "How do I exploit parallelism using the message passing interface (MPI)?"
objectives:
- "Explain how message passing allows performing computations in more than 1 computer at the same time."
- "Observe the effects of parallel execution of commands with a simple hostname call."
- "Measure the run time of parallel and MPI version of the implementation."
keypoints:
- "The MPI driver `mpirun` sends compute jobs to a set of allocated computers."
- "The MPI software then executes these jobs on the remote hosts and synchronizes their state/memory."
- "MPI assigns a rank to each process, usually the one with a rank of zero does the coordination"
- "MPI can be used to split a task into components and have several nodes run them."
---

Lola Lazy is now confident enough to work with the batch system of the cluster. She now turns her attention to the problem at hand, i.e. estimating the value of _Pi_ to very high precision. 

One of her more experienced colleagues has suggested to her, to use the _Message Passing Interface_ (in short: _MPI_) for that matter. As she has no prior knowledge in the field, accepting this advice is as good as trying some other technique on her how. She first explores the documentation of MPI a bit to get a feeling about the philosophy behind this approach. 

> ## Message Passing Interface
> A long time before we had smart phones, tablets or laptops, [compute clusters](http://www.phy.duke.edu/~rgb/brahma/Resources/beowulf/papers/ICPP95/icpp95.html) were already around and consisted of interconnected computers that had merely enough memory to show the first two frames of a movie (`2*1920*1080*4 Bytes = 16 MB`). 
> However, scientific problems back than were equally demanding more and more memory than today. 
> To overcome the lack of available hardware memory, [specialists from academia and industry](https://en.wikipedia.org/wiki/Message_Passing_Interface#History) came about with the idea to consider the memory of several interconnected compute nodes as one. Given a standardized software that synchronizes the various states of memory between the client/slave nodes during the execution of driver application through the network interfaces. With this performing large calculations that required more memory than each individual cluster node can offer was possible. Moreover, this technique by passing messages (hence _Message Passing Interface_ or _MPI_) on memory updates in a controlled fashion allowed to write parallel programs that were capable of running on a diverse set of cluster architectures.

![Schematic View of a Compute Cluster with 4 nodes (12 cores each)]({{ page.root }}/fig/cluster_schematic.svg)

Lola becomes curious. She wants to experiment with this parallelization technique a bit. For this, she would like to print the name of the node where a specific driver application is run. 

~~~
$ cat call_hostname.sh
#!/bin/bash

###                                                                                                                                                                                        
#SBATCH --job-name=mpi_hostname
#SBATCH --output=mpi_hostname.out.%J.%N
#SBATCH --error=mpi_hostname.err.%J.%N
###

mpirun hostname
~~~
{: .bash}

~~~
$ sbatch -n 4 mpi_hostname.sh
~~~
{: .bash}

The log file that is filled by the command above, contains the following lines after finishing the job:

~~~
ssb01
ssb01
ssb01
ssb01
~~~
{: .output}

The output makes her wonder. Apparently, the command was cloned and executed on the same host 4 times. If she increases the number of processors to a number larger than the number of CPU cores each of here nodes has, this might change and the distributed nature of `mpirun` will reveal itself.

~~~
$ sbatch -n 16 mpi_hostname.sh
~~~
{: .bash}

~~~
ssb01
ssb01
ssb01
ssb01
ssb01
ssb01
ssb01
ssb01
ssb01
ssb01
ssb01
ssb02
ssb01
ssb02
ssb02
ssb02
~~~
{: .output}

![Execution of `mpirun hostname` on a Compute Cluster with 4 nodes (12 cores each)]({{ page.root }}/fig/mpirunhostname_on_clusterschematic.svg)

As the figure above shows, 12 instances of `hostname` were called on `ssb01` and 4 more on `ssb02`. Strange though, that the last 5 lines are not ordered correctly. Upon showing this result to her colleague, the latter explains: even though, the `hostname` command is run in parallel across the 2 nodes that are used here, the output of her 16 `hostname` calls need to be merged into one output file (that she called `call_hostname.out`) at the end. This synchronization performed by the `mpirun` application is not guaranteed to happen in an ordered fashion (how could it be as the commands were issued in parallel). Her colleague explains, that the `hostname` application itself is not aware of _MPI_ in a way that it is not parallelized with it. Thus, the `mpirun` driver simply accesses the nodes that it is allowed to run on by the batch system and launches the `hostname` app. After that, `mpirun` collects the output of the executed commands at completion and writes it to the defined output file `call_hostname.out`.

Like a reflex, Lola asks how to write these MPI programs. Her colleague points out that she needs to program the languages that MPI supports, such as FORTRAN, C, C++, python and many more. As Lola is most confident with python, her colleague wants to give her a head start using `mpi4py` and provides a minimal example. This example is analogous to what Lola just played with. This python script called [`print_hostname.py`]({{ page.root }}/code/print_hostname.py) prints the number of the current MPI rank (i.e. the unique id of the execution thread within one mpirun invocation), the total number of MPI ranks available and the hostname this rank is currently run on.

Before we can run Mpi4py programs we need to install the module through pip3. Installing the pip module also requires the mpi module to be loaded. The following commands will install mpi4py. 

~~~
$ module load http-proxy
$ module load mpi
$ module load python/3.5.1
$ pip3 install --user mpi4py

~~~

Now we can run the program by putting the following into py_mpi_hostname.sh

~~~
#!/bin/bash


###                                                                                                                                                                                        
#SBATCH --job-name=py_mpi_hostname
#SBATCH --output=py_mpi_hostname.out.%J.%N
#SBATCH --error=py_mpi_hostname.err.%J.%N
###

module load mpi
module load python/3.5.1
mpirun python3 print_hostname.py
~~~
{: .bash}


and running it with:


~~~
$ sbatch -n 16 py_mpi_hostname.sh
~~~
{: .bash}

~~~
this is rank =  7 (total: 16) running on ssb028
this is rank =  0 (total: 16) running on ssb027
this is rank = 14 (total: 16) running on ssb030
this is rank =  6 (total: 16) running on ssb028
this is rank =  1 (total: 16) running on ssb027
this is rank = 15 (total: 16) running on ssb030
this is rank =  4 (total: 16) running on ssb028
this is rank =  2 (total: 16) running on ssb027
this is rank = 12 (total: 16) running on ssb030
this is rank =  5 (total: 16) running on ssb028
this is rank =  8 (total: 16) running on ssb029
this is rank = 13 (total: 16) running on ssb030
this is rank =  9 (total: 16) running on ssb029
this is rank = 10 (total: 16) running on ssb029
this is rank = 11 (total: 16) running on ssb029
this is rank =  3 (total: 16) running on ssb027
~~~
{: .output}

Again, the unordered output is visible. Now, the relation between the rank and the parameters `-n` to submit command becomes more clear. `-n` defines how many processors the current invocation of mpirun requires. With `-n 16` the rank can run from `0` to `15`.

> ## Does `mpirun` really execute commands in parallel?
>
> Launch the command `date` 16 times across your cluster. What do you observe? Play around with the precision of date through its flags (`+%N` for example) and study the distribution of the results.  
> 
> > ~~~
> > #!/bin/sh
> > ###                                                                                                                                                                                      > > #SBATCH --job-name=mpi_date
> > #SBATCH --output=mpi_date.out.%J.%N
> > #SBATCH --error=mpi_date.err.%J.%N
> > ###
> > module load mpi
> > mpirun date +%M:%S.%N
> > ~~~
> > {: .bash}
> {: .solution}
{: .challenge}

> ## Upgrade `print_hostname.py` and print the time-of-day as well
>
> Open the `print_hostname.py` script with your editor and use the python3 `datetime` module to print the time of day next to the host name and rank number.
> 
> > There are lots of possibly variations on this. Here's a simple one:
> > 
> > from datetime import datetime
> > print(str(datetime.now()))
> > 
> > or
> > 
> > import time
> > print(time.strftime("%d/%m/%Y %H:%M:%S",time.gmtime()))
> > 
> > or
> > 
> > import time
> > print(time.time())
> > 
> > this gives seconds and microseconds since January 1st 1970
> {: .solution}
{: .challenge}

To finalize this day's work, Lola wants to tackle distributed memory parallelization using the Message Passing Interface (MPI). For this, she uses the `mpi4py` library that is pre-installed on her cluster. She again starts from the [serial implementation]({{ page.root }}/code/serial_numpi.py). At first, she expands the include statements a bit. 

~~~
from mpi4py import MPI

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()
~~~
{: .python }

These 4 lines will be very instrumental through out the entire MPI program. The entire MPI software stack builds upon the notion of a communicator. Here, we see the MPI.COMM_WORLD communicator by which all processes that are created talk to each other. We will use it as a hub to initiate communications among all participating processes. Subsequently, we ask `comm` how many participants are connected by calling `comm.Get_size()`. Then we'll ask the communicator, what rank the current process is `comm.Get_rank()`. And with this, Lola has entered the dungeon of MPI. 

> ## Every Line Is Running in Parallel!
> As discussed in the previous section, a call to `<your scheduler> mpirun <your program>` will do the following:
>     - `mpirun` will obtain a list of available nodes from the scheduler
>     - mpirun will then `ssh` onto these nodes for you and instantiate a local mpirun there
>     - this local mpirun will execute `<your program>` in parallel to all the others and call every line of it from top to bottom
>     - only if your program reaches a statement of the form `comm.do_something(...)`, your program will start communicating through the mpi library with the other mpi processes; this communication can entail point-to-point data transfers or collective data transfers (that's why it's called 'message passing' because MPI does nothing else than provide mechanism to send messages around the cluster), depending on the type of communication, the MPI library might make your program wait until the all message passing has been completed
>In case you want to do something only on one rank specifically, you can do that by:
~~~
if rank == 0:
    print("Hello World")
~~~
{: .callout}

Pushing the implementation further, the list of `partitions` needs to be established similar to what was done in the parallel implementation above. Also a list for the results is created and all items are initialized to `0`.

~~~
if rank == 0:
    partitions = [ int(n_samples/size) for item in range(size)]
    counts = [ int(0) ] *size
else:
    partitions = None
    counts = None
~~~
{: .python}

In this example, you can see how the lists are only created on one rank for now (rank `0` to be precise). At this, point the contents of `partitions` and `counts` reside on rank `0` only. They now have to send to all other participating ranks.

~~~
partition_item = comm.scatter(partitions, root=0)
count_item = comm.scatter(counts, root=0)
~~~
{: .python}

Note how the input variable is `partitions` (aka a list of values) and the output variable is named `partition_item`. This is because, `mpi4py` returns only one item (namely the one item in `partitions` matching the rank of the current process, i.e. `partitions[rank]`) rather than the full list. Now, the actual work can be done.

~~~
count_item = inside_circle(partition_item)
~~~
{: .python}

This is the known function call from the serial implementation. After this, the results have to be communicated back again.

~~~
counts = comm.gather(count_item, root=0)
~~~
{: .python}

The logic from above is reverted now. A single item is used as input, aka `count_item`, and the result `counts` is a list again. In order to compute pi from this, the following operations should be restricted to `rank=0` in order to minimize redundant operations:

~~~
if rank == 0:
    my_pi = 4.0 * sum(counts) /n_samples
~~~
{: .python}

And that's it. Now, Lola can submit her first MPI job. Download the [full code]({{ page.root }}/code/mpi_numpi.py) to try it yourself.

~~~
#!/bin/bash

###                                                                                                                                                                                        
#job name
#SBATCH --job-name=mpi_numpi
#job stdout file
#SBATCH --output=mpi_numpi.out.%J.%N
#job stderr file
#SBATCH --error=mpi_numpi.err.%J.%N
###

module load python/3.5.1
module load mpi
mpirun python3 mpi_numpi.py 1000000000                           
 
$ sbatch -n 48 mpi_numpi.sh
~~~
{: .bash}

The output file `mpi_numpi.out` yields the following lines:

~~~
[     mpi version] required memory 11444.092 MB
[using  48 cores ] pi is 3.141679 from 1000000000 samples

real    0m3.924s
user    0m0.083s
sys     0m0.165s
~~~
{: .output}

Note here, that we are now free to scale this application to hundreds of cores if we wanted to. We are only restricted by Amdahl's law, the size of our compute cluster and any limits the administrators apply (on HPC Wales we can only use 25 nodes at once). Before finishing the day, Lola looks at the run time that her MPI job consumed. `3.92` seconds for a job that ran on six times as much cores as here parallel implementation before (which took `56s` for the same configuration). To test the performance and work out how many cores she should use she decided to write a small script which varied the number of cores being used. 

~~~
for i in {seq 1 48} ; do
    sbatch -n $i mpi_numpi.sh 
    sleep 2m
done
~~~
{: .bash}

She collects the results into a spreadsheet and graphs them. For comparison she also graphs the performance of the PyMP job running on a single node. These show that 

That is quite an achievement of the day!

![Performance vs Core Count MPI]({{ page.root }}/fig/mpi.svg)

![Performance vs Core Count PyMP]({{ page.root }}/fig/pymp.svg)

> ## Why isn't the graph smooth
> The MPI graph shown above doesn't a smooth curve like the PyMP one does when the number of cores are increased. Why might this be the case?
> > Some of the jobs will have run on the same nodes, others will have run across multiple nodes where data access is much slower. Exclusive use of the node wasn't requested either so other jobs may have impacted our performance.
> {: .solution}
{: .challenge}

> ## Use the batch system!
>
> Launch the serial and MPI version of the pi_estimate using the batch system. Compare the run times of each. 
> Note that with less than 100,000,000 samples there won't be significant differences between runtimes.
{: .challenge}

> ## Don't Stress the Network
>
> The MPI implementation given above transmits only the number of points in the circle to the main program. Rewrite the program so that each rank generates the random numbers and sends them back to rank 0. 
> 
> Submit the job and look at the time it took. What do you observe? Why did the run time change?
> > The performance gets significantly worse as a lot more data needs to be sent. When running on different nodes this will particularly bad as transferring data over the interconnect is much slower than locally.
> {: .solution}
{: .challenge}
