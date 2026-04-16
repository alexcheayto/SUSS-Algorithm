# SUSS-Algorithm

**SUSS** = **S**peeding **U**p **S**low **S**tart
Our goal was to replicate the SUSS algorithm created from this paper: 
> Mahdi Arghavani, Haibo Zhang, David Eyers, and Abbas Arghavani. 2024. SUSS: Improving TCP Performance by Speeding Up Slow-Start. In Proceedings of the ACM SIGCOMM 2024 Conference (ACM SIGCOMM '24). Association for Computing Machinery, New York, NY, USA, 151–165. https://doi.org/10.1145/3651890.3672234

We were able to recreate and analyze the differences between normal TCP and SUSS. In a smaller environment using python. 

To demonstrate network capabilities we also created a simple minet of 2 hosts. 

![[intro1.png]]

![[intro2.png]]
## Mininet and P4 Instructions

You will first need an environment setup for P4. We will be using Ubuntu image from this repository. If you need help setting up the environment for P4 or unsure just follow the instructions in the repository link below. 

https://github.com/jafingerhut/p4-guide/blob/master/bin/README-install-troubleshooting.md
Once the image is installed. Log into the virtual machine and cd into the tutorials directory. 

Then clone our repo. 

**git clone** https://github.com/alexcheayto/SUSS-Algorithm.git

cd into SUSS-Algorithm and run **make clean** and **make**

In the mininet terminal start two instances of hosts using **xterm h1 h2**

At this point you should have this outcome. 

![[mininetimage.png.png]]

For mininet you would have to update the two host ip addresses. In Node:h2 edit the file Server.py with nano  and change the HOST address to 10.0.2.2. In node:h1 do the same for the files SUSSsend.py, and TCPsend.py.

To collect accurate results make sure TCP.log and SUSS.log are empty. You can verify with cat. Data collected is stored in the log files.  

in Node:h2 run **python Server.py**
in Node:h1 run **python SUSSsend.py** once SUSSsend.py is finished run **python TCPsend.py**

this should be your final output with the numbers of course being different. 
![[mininetimage1.png.png]]

Data in the log files stores the time when an ACK packet is received. 