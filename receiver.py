import socket
from socket import AF_INET, SOCK_STREAM
import sys
import datetime
#Provided checksum functions and verifier
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
fullmesg = ""
#Set parameters
connection_id = sys.argv[1]
loss_rate = float(sys.argv[2])
corrupt_rate = float(sys.argv[3])
max_delay = int(sys.argv[4])
serverName = "128.119.245.12"
serverPort = 20000
time = datetime.datetime.now()
#print name and current time
print("Aylin Elmali " + time.strftime("%Y-%m-%d %H:%M:%S"))
clientString = "HELLO R " + str(loss_rate) + " " + str(corrupt_rate) + " " + str(max_delay) + " " + connection_id
print(clientString)
clientSocket = socket.socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))
clientSocket.send(clientString.encode())
ready = 0
#loop while waiting
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
        expseq = 0
        close = 0
        while(close == 0):
            #Create message
            seq = " "
            payload = "                    "
            try:
                modifiedMessage = clientSocket.recv(30)
                response = modifiedMessage.decode()
                #End loop
                if(response == ""):
                    close = 1
                    break
                print(response)
                list1 = response.split()
                key = list1[0]
                if(key == "ERROR"):
                    close = 1
                else:
                    #Check for corrupt message
                    if(checksum_verifier(response)):
                        numrec += 1
                        #Add to final full message
                        if(expseq == 0 and key == "0"):
                            expseq = 1
                            str1 = response[4:]
                            str2 = str1[:20]
                            fullmesg += str2
                        elif(expseq == 1 and key == "1"):
                            expseq = 0
                            str1 = response[4:]
                            str2 = str1[:20]
                            fullmesg += str2
                        ack = key
                        message = seq + " " + ack + " " + payload + " "
                        check = checksum(message)
                        send = message + check
                        print(send)
                        clientSocket.send(send.encode())
                        numsent += 1
                    else:
                        numcorr += 1
            except (ConnectionResetError):
                close = 1
    #Error message
    else:
        ready = 1
time = datetime.datetime.now()
#Checksum of full message
finalcheck = checksum(fullmesg)
out = "Aylin Elmali " + time.strftime("%Y-%m-%d %H:%M:%S") + " checksum:" + finalcheck + " sent:" + str(numsent) + " recvd:" + str(numrec) + " corrpt:" + str(numcorr)
print(out)
clientSocket.close()