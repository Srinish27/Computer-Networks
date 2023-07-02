import socket

recieverIP = "10.0.0.2"
recieverPort   = 20002
bufferSize  = 1024 #Message Buffer Size

# bytesToSend = str.encode(msgFromServer)

# Create a UDP socket
socket_udp = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind socket to localIP and localPort
socket_udp.bind((recieverIP, recieverPort))

print("UDP socket created successfully....." )

recieved_image = open("received.jpg","wb")
sequence = 0

while True: 
    
    #wait to recieve message from the server
    bytesAddressPair = socket_udp.recvfrom(bufferSize)
    #print(bytesAddressPair[0]) #print recieved message
    #split the recieved tuple into variables
    recievedMessage = bytesAddressPair[0]
    senderAddress = bytesAddressPair[1] 
    if(sequence==recievedMessage[0]):
        recieved_image.write(recievedMessage[1:])
        if(sequence==0):
            sequence = 1
        elif(sequence==1): 
            sequence = 0
        socket_udp.sendto(recievedMessage[0].to_bytes(1,'big'),senderAddress)
    elif(sequence!=(recievedMessage[0])):
        socket_udp.sendto(recievedMessage[0].to_bytes(1,'big'),senderAddress)
    #print them just for understanding~