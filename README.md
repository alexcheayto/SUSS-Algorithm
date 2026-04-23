# SUSS Replication

Our goal was to replicate performance gains of the SUSS algorithm from this SIGCOMM '24 paper: 
> Mahdi Arghavani, Haibo Zhang, David Eyers, and Abbas Arghavani. 2024. SUSS: Improving TCP Performance by Speeding Up Slow-Start. In Proceedings of the ACM SIGCOMM 2024 Conference (ACM SIGCOMM '24). Association for Computing Machinery, New York, NY, USA, 151–165. https://doi.org/10.1145/3651890.3672234

We were able to recreate and analyze the differences between normal TCP and SUSS on a small flow, albeit in a more constrained environment than the original authors, using Python and Mininet.

## SUSS Paper
**SUSS**: **S**peeding **U**p **S**low **S**tart

summary of paper

main contributions
^ observation of small flows

importance



## Chosen Claim

chosen claim (speific figure)

meaning of claim

replication feasability
^ contrast to other claims that are not feasible
say smth like "relevant to any TCP flow on any hardware, since all tcp connections will go through the slow-start phase"


## Paper Methodology

Specifically to the claim we are replicating not their whole cloud test stuff


## Our Methodology
To demonstrate network capabilities we also created a simple minet of 2 hosts. 

![intro1.png](https://github.com/alexcheayto/SUSS-Algorithm/blob/main/images/intro1.png)

![intro2.png](https://github.com/alexcheayto/SUSS-Algorithm/blob/main/images/intro2.png)

## Standalone Instructions

1. Open two terminals
2. Terminal A: run Server.py, the server will listen for packets and respond with ACKs 
3. Terminal B: run SUSSsend.py, then run Python3 TCPsend.py.

Logfiles are SUSS.log and TCP.log


For accurate results make sure TCP.log and SUSS.log are empty. Data stored is the time a packet recieved an ACK.
## Mininet and P4 Instructions

You will first need an environment setup for P4. We will be using Ubuntu image from this repository. If you need help setting up the environment for P4 or unsure just follow the instructions in the repository link below. 

https://github.com/jafingerhut/p4-guide/blob/master/bin/README-install-troubleshooting.md
Once the image is installed. Log into the virtual machine and cd into the tutorials directory. 

Then clone our repo. 

**git clone** https://github.com/alexcheayto/SUSS-Algorithm.git

cd into SUSS-Algorithm and run **make clean** and **make**

In the mininet terminal start two instances of hosts using **xterm h1 h2**

At this point you should have this outcome. 

![mininetimage.png.png](https://github.com/alexcheayto/SUSS-Algorithm/blob/main/images/mininetimage.png.png)

For mininet you would have to update the two host ip addresses. In Node:h2 edit the file Server.py with nano  and change the HOST address to 10.0.2.2. In node:h1 do the same for the files SUSSsend.py, and TCPsend.py.

To collect accurate results make sure TCP.log and SUSS.log are empty. You can verify with cat. Data collected is stored in the log files.  

in Node:h2 run **python Server.py**
in Node:h1 run **python SUSSsend.py** once SUSSsend.py is finished run **python TCPsend.py**

this should be your final output with the numbers of course being different. 
![mininetimage1.png.png](https://github.com/alexcheayto/SUSS-Algorithm/blob/main/images/mininetimage1.png.png)

Data in the log files stores the time when an ACK packet is received. 

## Our Results:
May differ from yours we have stored them in this google sheet available to anyone to view. We simply compared the speed by the time it took for packets to recieve an ACK for SUSS and regular TCP.
https://docs.google.com/spreadsheets/d/1Sn2767RZdpKYI-auLC4sWGnP_-sWX7QkhucRhfWD6gg/edit?usp=sharing

![results.png](https://github.com/alexcheayto/SUSS-Algorithm/blob/main/images/results.png)
