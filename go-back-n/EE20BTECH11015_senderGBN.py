import socket
import time

def add_sequence(chunk,sequence):
    sequence_byte = sequence.to_bytes(2,'big')
    return sequence_byte + chunk

senderIP = "10.0.0.1"
senderPort   = 20001
recieverAddressPort = ("10.0.0.2", 20002)
bufferSize  = 1024 #Message Buffer Size

# Create a UDP socket at reciever side
socket_udp = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
socket_udp.settimeout(0.025)
f = open("testFile.jpg","rb")
image = f.read()
chunks = []
for i in range(0,len(image),1022):
    temp = image[i:i+1022]
    chunks.append(temp)
sequence = 0
window_size = 128

i = 0
sent = 0
retrans = 0
t1 = time.time()
for j in range(window_size):
        msg = add_sequence(chunks[j],j)
        socket_udp.sendto(msg,recieverAddressPort)
        retrans += 1
        sent += 1

while (i<len(chunks)):
    try:
        msgFromServer = socket_udp.recvfrom(bufferSize)
        #print(msgFromServer[0])
        msgFromServer_int = int.from_bytes(msgFromServer[0],'big')
        if(i<=msgFromServer_int):
            i = msgFromServer_int+1
            while(sent<len(chunks) and sent<i+window_size):
                msg = add_sequence(chunks[sent],sent)
                socket_udp.sendto(msg, recieverAddressPort)
                sent += 1
                retrans += 1
    except:
        #print("packet lost")
        for j in range(window_size):
            if (i+j)<len(chunks):
                msg = add_sequence(chunks[i+j],i+j)
                socket_udp.sendto(msg,recieverAddressPort)
                retrans += 1
                sent += 1
t2 = time.time()
print('image sent')
print('Time taken is:',t2-t1)
print('Throughput is :',1172316/(1024*(t2-t1)))     
print('No.of retransmissions is:',retrans-len(chunks))