import socket
from socket import AF_INET, SOCK_STREAM
import sys
import datetime
#provided checksum functions and verifier
def checksum(msg):
    msg = msg.encode("utf-8")
    s = 0
    for i in range(0, len(msg), 1):
        s += msg[i]
    return format(s, '05d')
def checksum_verifier(msg):
    expected_packet_length = 30
    if len(msg) < expected_packet_length:
        return False
    content = msg[:-5]
    calc_checksum = checksum(content)
    expected_checksum = msg[-5:]
    if calc_checksum == expected_checksum:
        return True
    return False
numsent = 0
numrec = 0
numcorr = 0
numtimeout = 0
fullmesg = ""
#Set parameters
connection_id = sys.argv[1]
loss_rate = float(sys.argv[2])
corrupt_rate = float(sys.argv[3])
max_delay = int(sys.argv[4])
serverName = "128.119.245.12"
serverPort = 20000
transmission_timeout = int(sys.argv[5])
time = datetime.datetime.now()
#print name and current time
print("Aylin Elmali " + time.strftime("%Y-%m-%d %H:%M:%S"))
clientString = "HELLO S " + str(loss_rate) + " " + str(corrupt_rate) + " " + str(max_delay) + " " + connection_id
print(clientString)
clientSocket = socket.socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))
clientSocket.send(clientString.encode())
ready = 0
#loop for waiting
while(ready < 1):
    modifiedMessage = clientSocket.recv(1024)
    response = modifiedMessage.decode()
    print(response)
    list1 = response.split()
    key = list1[0]
    if(key == "WAITING"):
        ready = 0
    #Connection success
    elif(key == "OK"):
        ready = 1
        time = datetime.datetime.now()
        print("Connection Established: " + time.strftime("%Y-%m-%d %H:%M:%S"))
        seq = 0
        ack = 1
        #Open file
        f = open("C:/Users/skywa/OneDrive/Documents/CompSci453/declaration.txt", "r")
        for x in range (0, 10):
            #Create message
            payload = f.read(20)
            #Add to final full message
            fullmesg += payload
            message = str(seq) + " " + str(ack) + " " + payload + " "
            check = checksum(message)
            send = message + check
            done = 0
            #loop until ready to send next data
            while(done == 0):
                clientSocket.send(send.encode())
                print(send)
                numsent += 1
                clientSocket.settimeout(transmission_timeout)
                #To avoid Blocking IO Error
                if(transmission_timeout == 0):
                    clientSocket.setblocking(1)
                try:
                    modifiedMessage = clientSocket.recv(30)
                    response = modifiedMessage.decode()
                    numrec += 1
                    print(response)
                    #Check for corrupt message
                    if(checksum_verifier(response)):
                        list1 = response.split()
                        key = list1[0]
                        #Check for correct ACK
                        if(seq == 1 and key == "1"):
                            done = 1
                        elif(seq == 0 and key == "0"):
                            done = 1
                    else:
                        numcorr += 1
                #Timeout
                except socket.timeout:
                    numtimeout += 1
            #Change seq #
            if(seq == 0):
                seq = 1
                ack = 0
            else:
                seq = 0
                ack = 1
        f.close()
    #Error message
    else:
        ready = 1
time = datetime.datetime.now()
#Checksum of full message
finalcheck = checksum(fullmesg)
out = "Aylin Elmali " + time.strftime("%Y-%m-%d %H:%M:%S") + " checksum:" + finalcheck + " sent:" + str(numsent) + " recvd:" + str(numrec) + " corrpt:" + str(numcorr) + " tmouts:" + str(numtimeout)  
print(out)
clientSocket.close()