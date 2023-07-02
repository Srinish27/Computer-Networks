import socket
import time

def add_sequence(chunk,sequence):
    return sequence.to_bytes(1,'big')+chunk

senderIP = "10.0.0.1"
senderPort = 20001
recieverAddressPort = ("10.0.0.2", 20002)
bufferSize = 1024 #Message Buffer Size

# Create a UDP socket at reciever side
socket_udp = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
socket_udp.settimeout(0.03)
f = open("testFile.jpg","rb")
image = f.read()
chunks = []
for i in range(0,len(image),1023):
    temp = image[i:i+1023]
    chunks.append(temp)
sequence = 0
retrans = 0
t1 = time.time()
for i in chunks:
    msg = add_sequence(i,sequence)
    socket_udp.sendto(msg, recieverAddressPort)
    retrans += 1
    #print(sequence)
    # # print(msg[0])
    #wait for reply message from reciever
    flag = True
    while True:
        try:
            msgFromServer = socket_udp.recvfrom(bufferSize)
            #print(int.from_bytes(msgFromServer[0],'big'))
            if(int.from_bytes(msgFromServer[0],'big')==msg[0]):
                break
            # print("packet received")
            else:
                socket_udp.sendto(msg, recieverAddressPort)
                retrans += 1
        except:
            #print("packet lost")
            socket_udp.sendto(msg, recieverAddressPort)
            retrans += 1
            
    if(sequence==1):
        sequence = 0
    elif(sequence==0):
        sequence = 1

t2 = time.time()
print('image sent')
print('Time taken is:',t2-t1)
print('Throughput is :',1172316/(1024*(t2-t1)))     
print('No.of retransmissions is:',retrans-len(chunks))
