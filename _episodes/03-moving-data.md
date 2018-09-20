---
title: "Filesystems and Storage"
author: "Colin Sauze"
teaching: 15
exercises: 30
questions: 
 - "Where can I store my data?"
 - "What is the difference between scratch and home filestore?"
objectives: 
 - "Understand the difference between home and scratch directories"
 - "Understand how to copy files between your computer and your SCW home/scratch directories"
keypoints:
 - "Scratch and home are per site, no common storage between sites."
 - "Scratch is faster and has no quotas, its not backed up. home is slower, smaller but backed up"
---


# Filesystems and Storage

## What is a filesystem?
Storage on most compute systems is not what and where you think they are! Physical disks are bundled together into a virtual volume; this virtual volume may represent one filesystem, or may be divided up, or partitioned, into multiple filesystems. And your directories then reside within one of these fileystems. Filesystems are accessed over the network through mount points.

There are multiple storage/filesystems options available for you to do your work. The most common are:
* home: where you land when you first login. 50 GB per user. Slower access, backed up. Used to store your work long term. 
* scratch: temporary working space. Faster access, not backed up. No quota, but old files might get deleted. DON'T STORE RESULTS HERE!

Here's a synopsis of filesystems on HPC Wales:

|Name|Path|Default Quota|Disk Size|Backed Up|Access Speed|
|------|---|----|-----|---|-----|
|Bangor Home|/home/user.name|N/A|8TB|Yes|~250 Mbyte/sec|
|Bangor Scratch|/scratch/user.name|N/A|1TB|No|~280 MByte/sec|
|Cardiff Home|/home/user.name|50GB|195TB|Yes|~350 Mbyte/sec|
|Cardiff Scratch|/scratch/user.name|N/A|170TB|No|~800 Mbyte/sec|
|Cardiff Group|/space0[0-9]/HPCWXXX|Negotiable|195TB (same disk as home)|Yes|~350 Mbyte/sec|
|Swansea Home|50GB|/home/user.name|N/A|195TB|Yes|~350 Mbyte/sec|
|Swansea Grooup|/space0[0-9]/HPCWXXX|Negotiable|N/A|195TB (same disk as home)|No|~350 Mbyte/sec|
|Swansea Scratch|/scratch/user.name|N/A|336TB|No|336TB|~800 Mbyte/sec|


New filesystems will be delivered on Super Computing Wales. Swansea home directories on SCW WILL NOT BE BACKED UP!!!!

**Important!! Ensure that you don't store anything longer than necessary on scratch, this can negatively affect other people’s jobs on the system.**


# Accessing your filestore

## How much quota do I have left on my home directory?

Login to a head node (e.g. sunbird.swansea.ac.uk or hawklogin.cf.ac.uk) and run the ```myquota``` command. This will tell you how much space is left in your home directory. 

~~~
$ myquota
~~~
{: .bash}

~~~
Disk quotas for group colin.sauze (gid 16782669): 
     Filesystem  blocks   quota   limit   grace   files   quota   limit   grace
cfsfs001-s03:/nfsshare/exports/space03
                   192M  51200M  53248M            2529    500k    525k    
~~~
{: .output}
    

## How much scratch have I used?

The ```df``` command tells you how much disk space is left. The ```-h``` argument makes the output easier to read, it gives human readable units like M, G and T for Megabyte, Gigabyte and Terrabyte instead of just giving output in bytes. By default df will give us the free space on all the drives on a system, but we can just ask for the scratch drive by adding ```/scratch``` as an argument after the ```-h```. 

~~~
$ df -h /scratch
~~~
{: .bash}

~~~
Filesystem                                Size  Used Avail Use% Mounted on
172.2.1.51@o2ib:172.2.1.52@o2ib:/scratch  692T   57T  635T   9% /scratch
~~~
{: .output}

## Copying data from your PC to SCW

You can copy files to/from your SCW home and scratch drives using the secure copy protocol (SCP) or secure file transfer protocol (SFTP) and connecting to Sunbird or Hawk. 

### Copying data using the command line

Use the ```sftp``` command and connect to the system. This takes the argument of the username followed by an @ symbol and then the hostname. Optionally you can specify what directory to start in by putting a ```:``` symbol after this and adding the directory name. The command below will start in ```/home/s.jane.doe/data```, if no directory is specified then sftp defaults to your home directory. 

~~~
sftp s.jane.doe@sunbird.swansea.ac.uk:/home/s.jane.doe/data
~~~
{: .bash}


~~~
s.jane.doe@sunbird.swansea.ac.uk's password: 
Connected to sunbird.swansea.ac.uk.
Changing to: /home/s.jane.doe/data
sftp> ls
~~~
{: .output}


The ```sftp``` and ```scp``` commands should be available on all Linux and Mac systems. On Windows systems they can be made available if you install the Linux Subsystem for Windows (Windows 10 only), the Github command line (CHECK ME).
Aberystwyth University Windows desktops already have these commands installed. 


### Copying data using Filezilla

Filezilla is a graphical SCP/SFTP client available for Windows, Mac and Linux. You can download it from https://filezilla-project.org/download.php?type=client

Open filezilla and click on file menu and choose ```Site Manager```. 

![Transferring files using FileZilla](../fig/filezilla1.png)

A new site will appear under "My Sites". Name this site "Super Computing Wales" by clicking on Rename. Then enter "sunbird.swansea.ac.uk" or "hawklogin.cf.ac.uk" as the Host, your username as the user name and choose "Ask for password" as the logon type. Then click Connect. You should now be prompted for your password, go ahead and enter your HPC Wales password and click Ok. 

![Transferring files using FileZilla](../fig/filezilla2.png)

You should now have some files in the right hand side of the window. These are on the remote system, the list on the left hand side is your local system.

![Transferring files using FileZilla](../fig/filezilla3.png)

Files can be transferred either by dragging and dropping them from one side to the other. Or you can right click on a remote file and choose "Download" or a local file and choose "Upload". 

![Transferring files using FileZilla](../fig/filezilla4.png)
![Transferring files using FileZilla](../fig/filezilla5.png)

You can change directory on the remote host by typing a path into the "Remote site:" box. For example type in ```/scratch/user.name``` (where user.name is your username) to access your scratch directory. 

![Transferring files using FileZilla](../fig/filezilla6.png)



# Exercises

> ## Using the `df` command. 
> 1. Login to a head node
> 2. Run the command `df -h`.
> 3. How much space does /scratch have left? 
> 4. If you had to run a large job requiring 10TB of scratch space, would there be enough space for it?
{: .challenge}

> ## Using the `myquota` command.
> 1. Login to a head node.
> 2. Run the `myquota` command. 
> 3. How much space have you used and how much do you have left? 
> 4. If you had a job that resulted in 60GB of files would you have enough space to store them?
{: .challenge}

> ## Copying files.
> 1. Login to a head node.
> 2. Create a file called hello.txt by using the nano text editor (or the editor of your choice) and typing `nano hello.txt`. Enter some text into the file and press Ctrl+X to save it. 
> 3. Use either Filezilla or SCP/SFTP to copy the file to your computer. 
> 4. Create a file on your computer using a text editor. Copy that file to your SCW home directory using Filezilla or SCP/SFTP and examine its conents with nano on the head node. 
{: .challenge}
