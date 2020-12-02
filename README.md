# Reliable-Data-Transfer
This project implements an rdt 3.0 protocol with a sender and receiver to correctly transfer the first 200 characters of the Declaration
of Independence. The sender and receiver are both implemented as TCP clients that connect with a server at gaia.cs.umass.edu. The sender
is invoked by sender.py <connection_id> <loss_rate> <corrupt_rate> <max_delay> <transmission_timeout> and the receiver is invoked by
receiver.py <connection_id> <loss_rate> <corrupt_rate> <max_delay>. The loss and corrupt rates range from 0.0 to 1.0 and determine how 
likely it is that a packet will be lost or corrupted. Max delay ranges from 0 to 5 and determines delay in seconds at the server. The 
transmission timeout determines how long the sender should wait for an acknowledgement before re-sending. Each packet contains a sequence
number, ACK number, 20 characters of the text, and a checksum of the data to check for corruption. The sender will send data and wait for
an ACK from the receiver. The sequences numbers and ACK numbers alternate between 0 and 1. The sender will re-send packets on a timeout and
will not move on to the next 20 bytes until an uncorrupted ACK with the correct number is received. The receiver will not send the next ACK
until it receives an uncorrupted packet with the correct sequence number. Upon starting, both the sender and receiver print my name and the
date and time. Once connected to the server, they will print the current time and a confirmation of the connection. Once all data is transferred
both will print my name, the date and time, and a checksum of all 200 characters as well as the total number of packets send and received, the
number of corrupted packets, and the number of timeouts on the sender side.
