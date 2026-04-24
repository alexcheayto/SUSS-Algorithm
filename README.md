# SUSS Replication

Our goal was to replicate performance gains of the SUSS algorithm from this SIGCOMM '24 paper:

`Mahdi Arghavani, Haibo Zhang, David Eyers, and Abbas Arghavani. 2024. SUSS: Improving TCP Performance by Speeding Up Slow-Start. In Proceedings of the ACM SIGCOMM 2024 Conference (ACM SIGCOMM '24). Association for Computing Machinery, New York, NY, USA, 151–165. https://doi.org/10.1145/3651890.3672234`

SUSS Repo: https://github.com/SUSSdeveloper/SUSSprg


We were able to recreate and analyze the differences between normal TCP and SUSS on a small flow, albeit in a more constrained environment than the original authors, using Python and Mininet.
## SUSS: *S*peeding *U*p *S*low *S*tart
SUSS is an improvement to the SlowStart phase of TCP-based congestion control algorithms. 

Traditional SlowStart works by sending double the amount of packets each round trip time (RTT) by increasing the congestion window (cwnd). This exponential growth continues until a specific threshold is reached or packet loss is detected. While "exponential" sounds fast, due to large bandwidth capacity of modern hardware, it often takes dozens of rounds for a flow to reach it's optimal cwnd, resulting in bandwidth underutilization.

SUSS works by splitting each RTT of SlowStart into 3 subphases:
- Clock: Send packets in a burst similar to traditional TCP SlowStart.
- Guard: Delay to allow for accurate time measurement of each round.
- Pacing: Send additional packets, evenly spaced.

The key idea is this: SUSS can use the ACKs from the clock packets to predict whether or not it is safe to continue exponential growth, and by how much. This allows for highly accelerated increases in cwnd for a connection, which means a flow will achieve its fair share of bandwidth much faster than with traditional SlowStart.
wha
TCP-SlowStart's inefficiency may at first sound like a small problem, but as the authors observe, there is great potential for FCT (Flow Completion Time) improvement with small flows such as web pages, photos, and even short videos. For example, loading a website with many elements, where each element is sent in its own flow. SUSS is significant since even if the overall data transmitted was many megabytes, the proportion of time spent in the SlowStart phase is high due to the many small flows it consisted of.

# Chosen Claim
In the paper the authors claim:

*"SUSS achieves over 20% improvement in flow completion time in all 
experiments with flow sizes less than 5 MB and RTT larger than 50 ms."*

Later on, they present Figure 10, depicting a comparison between two CUBIC variants: one with SUSS and one with traditional SlowStart.
<img width="316" height="216" alt="image" src="https://github.com/user-attachments/assets/6049fa6a-4e31-490d-80d8-f911f1d73aff" /> `Figure 10.`

This figure shows that SUSS helps the flow achieve its optimal cwnd much sooner when compared to traditional SlowStart. They highlight that at time t=2s, the SUSS flow has delivered 7MB of data and has already exited SlowStart, while the non-SUSS flow has only delivered 2MB of data and has yet to exit SlowStart.
The claim and figure are feasible to replicate for us, especially compared to other claims that involve testing across multiple servers in different regions. The performance of small flows is relevant to any TCP flow on any hardware, since all TCP connections will go through the slow-start phase at least once when starting up, and is even more so when considering smaller flows, since they spend a larger proportion of their FCT in the SlowStart phase.

# Paper Methodology
The authors implement SUSS into the Linux Kernel (v5.19.10) by modifying its implementation of the CUBIC congestion control algorithm, along with other code (in order to help facilitate the modification, and to actively report data. CUBIC’s code was modified to switch the Gi parameter from two to four, making it such that the cwnd quadruples (rather than doubles) for every RTT, making the flow accelerate significantly faster (under ideal conditions). To implement the authors’ state, you’d need to recompile the linux kernel’s source code and follow their installation guide in the github repo listed above.
A flowchart depicting the SUSS algorithm and their modifications to HyStart (which assists with packet pacing and growth estimation) are presented in Figures 7 & 8:
<img width="406" height="525" alt="image" src="https://github.com/user-attachments/assets/4b42d8f7-98b0-40cf-b6da-8689bb39d57c" /> <img width="451" height="626" alt="image" src="https://github.com/user-attachments/assets/20a8c508-8680-4ef0-ad81-cbdc22da57f4" />

To evaluate the effectiveness of SUSS, the authors measured multiple metrics, including; the RTT during flows, FCT of each flow, and delivery rate. They deployed a SUSS-capable webserver in different cloud servers across geographic regions. By doing so, they were able to test how well SUSS could perform on various different networks, topologies, or architectures. 


# Our Methodology
Our goal was only to utilize SUSS and draw comparisons to TCP; we did not do a one to one recreation. As well as did not use the same technologies or tools as mentioned in the paper. We also focused on only measuring FCT, flow completion time. 

We recreated the SUSS algorithm in python. Our source code can be found in this github repository: https://github.com/alexcheayto/SUSS-Algorithm.  We also recreated basic TCP protocol and to measure the differences we clocked and timestamped the instance that a ACK has been received, which gives us our FCT of the payload.  After testing in python we added a mininet instance. Below was the topology we decided to use. All instructions to recreate our setup are in the github. 
We tracked and saved records into the log file and ran the experiment with 4 varying process delays for a total of 500 packets. To analyze for smaller flow we used 128 packets. 
To demonstrate network capabilities we also created a simple mininet of two hosts.
<img width="320" height="93" alt="image" src="https://github.com/user-attachments/assets/e196123c-e1e5-4ea9-8107-40256a0ff554" />`Diagram of our topology`

<img width="360" height="432" alt="image" src="https://github.com/user-attachments/assets/82c820c5-45fd-4601-a58e-f800f507a785" />`Terminal Screenshots of both hosts`



## Our Divergences
Some divergences from our setup compared to theirs include: us not accounting for congestion, and testing how congestion impacts the FCT for SUSS and TCP. This was mostly due to poor self evaluations of our skills and a tight time constraint.. 

For future experiments we will be sure to implement and create a more realistic environment. Especially since SUSS is designed for congestion control. Other differences would be the scale of their experiment with multiple servers and clients, something we are lacking. Instead we opted for a small mininet topology. We also added more simplification than what would be realistic and in a real world network. We added fixed roundLength, and had a slower network to allow easier tracking and measurement. 


# Lessons Learned:
We learned our replication isn’t too close or similar to the reference paper and implementation can be rather challenging. We were unable to recreate a similar environment such as having more clients and servers, or adding congestion to our network. We also added more simplifications such as adding fixed roundLength, one packet at a time, and we had a slower network for us to track more easily. Despite our differences we were still able to reach the same conclusion the authors of “SUSS:Improving TCP Performance by Speeding up Slow-Start” found.  We found SUSS is not suss and does have a better flow completion time when compared to CUBIC TCP.



# Running the Program
Standalone Instructions
1. Open two terminals
2. Terminal A: run Server.py, the server will listen for packets and respond with ACKs
3. Terminal B: run SUSSsend.py, then run Python3 TCPsend.py.
Logfiles are SUSS.log and TCP.log

For accurate results make sure TCP.log and SUSS.log are empty. Data stored is the time a packet receives an ACK.

## Mininet and P4 Instructions
You will first need an environment setup for P4. We will be using Ubuntu image from this repository. If you need help setting up the environment for P4 or unsure just follow the instructions in the repository link below.
https://github.com/jafingerhut/p4-guide/blob/master/bin/README-install-troubleshooting.md 
Once the image is installed. Log into the virtual machine and cd into the tutorials directory.
Clone our repo: `git clone https://github.com/alexcheayto/SUSS-Algorithm.git`
`cd` into SUSS-Algorithm and run `make clean` and `make`
In the mininet terminal start two instances of hosts using `xterm h1 h2`
At this point you should have this outcome:
<img width="544" height="428" alt="image" src="https://github.com/user-attachments/assets/93af2cd1-b5b7-47c9-9ad4-ff5572fa8318" />`A screenshot of what you would be seeing on your machine`

For mininet you would have to update the two host ip addresses. In Node:h2 edit the file Server.py with nano and change the HOST address to 10.0.2.2. In node:h1 do the same for the files SUSSsend.py, and TCPsend.py.
To collect accurate results make sure TCP.log and SUSS.log are empty. You can verify with cat. Data collected is stored in the log files.
in Node:h2 run python Server.py in Node:h1 run `python SUSSsend.py` once SUSSsend.py is finished run `python TCPsend.py`

This should be your final output with the numbers of course being different:
<img width="657" height="417" alt="image" src="https://github.com/user-attachments/assets/f6762779-7eb3-43f8-b986-0ee80bc3cf09" />


Data in the log files stores the time when an ACK packet is received.


# Our Results:
May differ from yours. We have stored them in this google sheet available to anyone to view. We simply compared the speed by the time it took for packets to receive an ACK for SUSS and regular TCP. 
Here below you can view all of the data we have collected in the spreadsheet below. 
https://docs.google.com/spreadsheets/d/1Sn2767RZdpKYI-auLC4sWGnP_-sWX7QkhucRhfWD6gg/edit?usp=sharing
<img width="659" height="329" alt="image" src="https://github.com/user-attachments/assets/77e640de-a63f-4781-b2b9-145316485322" />

What we found is that SUSS did have a better flow completion time when compared to TCP CUBIC during small flows. Similar to their result and comparison. 
<img width="640" height="439" alt="image" src="https://github.com/user-attachments/assets/4f53638f-a0b7-45c8-ae52-60089488feff" />

