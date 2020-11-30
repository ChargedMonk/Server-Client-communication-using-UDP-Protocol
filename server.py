import socket
from serverApp import *

def new_user(username,password):
    with open('credentials.txt','a') as file:
        file.write(username+":"+password+'\n')
    print("user registered\nUsername:",username)
    print("Password:",password)


def validate(username,password):
    if username==password=='admin':
        return True
    with open('credentials.txt') as file:
        for line in file:
            line = line.strip().split(':')
            if line[0]==username:
                if line[1] == password:
                    return True
    return False

localIP     = "127.0.0.1"
localPort   = 20001
bufferSize  = 5120
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPServerSocket.bind((localIP, localPort))
print("UDP server up and listening")
user = 'guest'
while(True):
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    message = bytesAddressPair[0]
    address = bytesAddressPair[1]
    message = message.decode("UTF-8").split('.~.')
    if len(message) == 1:
        message = message[0]
        print("user =",user)
        if user == 'guest':
            msgFromServer = serverReply(message,2)
        else:
            msgFromServer = serverReply(message)
        bytesToSend = str.encode(msgFromServer)
        UDPServerSocket.sendto(bytesToSend, address)
    else:
        if message[1]=='exit':
            UDPServerSocket.sendto(str.encode("Exiting..."),address)
            exit()
        elif message[0] == 'new':
            new_user(message[1],message[2])
            server_message = str.encode('User registered')
            UDPServerSocket.sendto(server_message,address)
        elif message[0] == 'guest':
            user = 'guest'
            server_message = str.encode('Guest access')
            UDPServerSocket.sendto(server_message,address)
        elif message[0] == 'credentials':
            print("login attempt")
            print("username:",message[1])
            print("password:",message[2])
            if(validate(message[1],message[2])):
                print('Login successful')
                server_message = str.encode('1')
                user = 'authorized'
                UDPServerSocket.sendto(server_message,address)
            else:
                print("Login unsuccessful")
                server_message = str.encode('0')
                UDPServerSocket.sendto(server_message,address)
