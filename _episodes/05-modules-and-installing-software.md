---
title: "Working with Modules and Installing Software"
author: "Colin Sauze"
teaching: 15
exercises: 30
questions: 
 - "How do I get access to additional software?"
objectives: 
 - "Understand how to load a module"
 - "Understand how to install pip packages for Python"
keypoints:
 - "A lot of software is only available by loading extra modules. This helps prevent problems where two packages are incompatible."
 - "Python3 is one such package."
 - "If you want to install pip packages use the --user option to store the packages in your home directory."
---

# Using & installing software

On most cluster systems, all the software installed is not immediately available for use;
instead, it is loaded into your environment incrementally using a module system. 

The module command controls this. 
You can get a list of available software with the `module avail` command. This should return a long list of available software.

One common piece of software that isn't installed on SCW (without a module) is Python version 3. If we attempt to run `python3` from the command line it will respond with an error:

~~~
[s.jane.doe@sl1 ~]$ python3
~~~
{: .bash}

~~~
-bash: python3: command not found
~~~
{: .output}

**Note that the head node and the compute nodes have identical configurations in terms of what software is available, so you can discover if your program will run from the head node**

From the output of the `module avail` command there should have been an entry `python/3.7.0` in the `/app/modules/langauges` section near the top. Lets go ahead and load this using the 
Lets load Python version 3.7.0 as a module and attempt to run the python3 command. This should start a Python3 interpreter, we can exit python by either pressing Ctrl+d or typing `exit()` and pressing enter. 

~~~
[s.jane.doe@sl1 ~]$ module load python/3.7.0
[s.jane.doe@sl1 ~]$ python3
Python 3.7.0 (default, Jul 13 2018, 10:08:05) 
[GCC Intel(R) C++ gcc 4.8.5 mode] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> exit()
[s.jane.doe@sl1 ~]$
~~~
{: .bash}

> ## Legacy HPC Wales and Raven Modules 
> All of the old modules which were available on HPC Wales and the old Cardiff Raven system 
> are available by running either `module load hpcw` or `module load raven` (Raven modules are only available on Hawk).
> Please note that much of this software is outdated and may by suboptimal as its not compiled
> to take advantage of the newer CPU architectures on Super Computing Wales.
{: .callout}


## Installing Python modules

Python is a popular language for researchers to use and has modules (aka libraries) that do all kinds of useful things, but sometimes the module you need won't be installed. Many modules can be installed using the pip (or pip3 with python3) command. 

We also don't have permissions to install pip modules for the whole system, so we need to give pip the `--user` argument which tells us to install in our home directory. 

~~~
[s.jane.doe@sl1 ~]$  pip3 install --user <modulename>
~~~
{: .bash}

Lets install the Sci Kit Learn (sklearn)  module, this is a module which is useful for machine learning tasks but isn't installed on HPCW by default. 

~~~
[s.jane.doe@sl1 ~]$  pip3 install --user sklearn
Collecting sklearn
  Downloading sklearn-0.0.tar.gz
Collecting scikit-learn (from sklearn)
  Downloading scikit_learn-0.19.1-cp35-cp35m-manylinux1_x86_64.whl (12.2MB)
    100% | ************* | 12.2MB 50kB/s 
Installing collected packages: scikit-learn, sklearn
  Running setup.py install for sklearn ... done
Successfully installed scikit-learn-0.19.1 sklearn-0.0
You are using pip version 10.0.1, however version 18.0 is available.
You should consider upgrading via the 'pip install --upgrade pip' command.
[s.jane.doe@sl1 ~]$
~~~
{: .bash}

Lets test the sklearn has been installed by loading its example digits dataset:

~~~
[s.jane.doe@sl1 ~]$ python3
Python 3.5.1 (default, Jun 22 2016, 13:43:55) 
[GCC Intel(R) C++ gcc 4.4.7 mode] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from sklearn import datasets
>>> digits = datasets.load_digits()
>>> print(digits.data)
[[  0.   0.   5. ...,   0.   0.   0.]
 [  0.   0.   0. ...,  10.   0.   0.]
 [  0.   0.   0. ...,  16.   9.   0.]
 ..., 
 [  0.   0.   1. ...,   6.   0.   0.]
 [  0.   0.   2. ...,  12.   0.   0.]
 [  0.   0.  10. ...,  12.   1.   0.]]
~~~
{: .bash}

The outputted data is part of the contents from sklearn. 

## How to install other software yourself

*For Perl & Python modules or R packages*, we encourage you to set up directories in your
home and/or lab folders for installing your own copies locally. Instructions on how to install these are available from the [How To](https://portal.supercomputing.wales/index.php/index/how-to-guides-archive/) pages on the Super Computing Wales portal.

## Requesting additional software 

*If software you need is not installed*, we encourage you to do local installs in your home
or lab folder for bleeding-edge releases, software you are testing, or software used
only by your lab. For programs that are commonly used by your domain, field, 
or department, please submit a 
[software install request](email:support@supercomputingwales.ac.uk).
Note that due to demand and the complex nature of software installs, it may take a while for us to complete these requests. 

Commercial software will require the appropriate licenses. 


# Exercises

> ## Running a python script. 
> plot.py script used in the exercises.
> ~~~
> import matplotlib as mpl
> mpl.use('Agg') #set the backend to Agg to make a png file instead of displaying on screen
> import matplotlib.pyplot as plt
> plt.plot(range(10))
> plt.savefig('temp.png')
> ~~~
> {: python}
> 
> plot.sh script used in the exercises.
> 
> ~~~
> #!/bin/bash --login
> ###
> #job name
> #SBATCH --job-name=plotgraph
> #job stdout file
> #SBATCH --output=plotgraph.out.%J
> #job stderr file
> #SBATCH --error=plotgraph.err.%J
> #maximum job time in D-HH:MM
> #SBATCH --time=0-00:01
> #number of tasks you are requesting 
> #SBATCH --ntasks=1
> #memory per process in MB 
> #SBATCH --mem=2
> #SBATCH --nodes=1
> ###
> module load python/3.7.0
> python3 plot.py
> ~~~
> {: .bash}
> 1. Create a new file using nano and call it plot.py. It should contain the text from the Python script shown above.
> 2. Create a new job submission script containing the text from the Bash script shown above, call it plot.sh. 
> 3. Run the job with `sbatch plot.sh`. Did the job complete successfully? Are there any errors in the error file? 
> 4. Fix the cause of the errors by adjusting (or removing) the appropriate parameter. 
> 5. Copy back the resulting file, temp.png using SCP or SFTP and view it on your computer. 
> 6. Add the following lines to the Python script (between the plt.plot line and the plt.savefig line) to make it embed the job ID into the title of the image:
> `import os`, `jobid=str(os.environ.get('SLURM_JOBID'))` and  `plt.title('Job id '+jobid)`
> run the job again and look at the output image. A list of other environment variables can be found at https://www.glue.umd.edu/hpcc/help/slurmenv.html, try some of these instead.
>
> > ## Solution
> > 1. You will get errors about the amount of memory being used. These might show up as a segmentation fault rather than a memory error. For some reason this script can be very slow to run sometimes, so increasing the timeout can help too. But only do this if you are getting timeout errors. Around 50MB of memory and 5 minutes should be enough.
> > 2. Your python code should now read:
> >
> > ~~~
> > import matplotlib as mpl
> > mpl.use('Agg') #set the backend to Agg to make a png file instead of displaying on screen
> > import os
> > import matplotlib.pyplot as plt
> > plt.plot(range(10))
> > jobid=str(os.environ.get('SLURM_JOBID'))
> > plt.title('Job id '+jobid)
> > plt.savefig('temp.png')
> > ~~~
> > {: .bash}
> >
> {: .solution}
{: .challenge}

