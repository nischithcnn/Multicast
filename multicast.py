'''*********************************************************************************
  multicast SOURCE FILE - Nischith Nanjundaswamy (nischith.cnn@gmail.com)
  CREATED: 11/8/2018
  This code provides Server and Client socket functionality with Multicasting.
  Server sends beacon message to multicast address.
  Client will send the ACK to server address .
  Server will list the number of active clients.If the active client list is more than 1 ,
  then the server sends file data to multicast address.
  At the end of file data, server sends a goodbye message.
  Client reads the multicast message and sends the ACK to server and closes its connection.
*************************************************************************************'''
import socket
import logging as log
import sys
import struct
import time

message = {"GOODBYE":"goodbye","FAREWELL":"farewell",
           "EXIT":"exit","OK":"ok"}
HOST_IP = '10.10.2.10'
PORT = 2145
Timer = 5000
fileData =[]
beacon = 'Hi I am server!!!'

# udp server socket fucntion
# accepts port and file pointer as the argument
def udp_server_socket(mcast, f):
    try:
        # Create server socket and bind to host and port
        server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        log.info("UDP socket created successfuly \n")

        # set TTL value
        ttl = struct.pack('b', 2)
        server.setsockopt(socket.SOL_IP, socket.IP_MULTICAST_IF,socket.INADDR_ANY)
        server.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
        multicast_group = (mcast, PORT)

        # send data to multicast group
        for lines in f:
            fileData.append(lines.decode(('utf-8'),'ignore'))
            print(fileData)
        fileData.append("goodbye")
        length = len(fileData)
        clientList = []

        while len(clientList) <= 1:
            print("Sending server message to multicast group", beacon)
            sent = server.sendto(beacon, multicast_group)
            msg_sent_time = int(round(time.time() * 1000))
            current_time = int(round(time.time() * 1000))

            while True:
                del clientList[0:len(clientList)]
                while (current_time - msg_sent_time <= Timer):
                    server.setblocking(False);
                    try:
                        data, addr = server.recvfrom(255)
                        if data != None:
                            rcv_msg = data.decode("utf-8")
                            print("Message from client: ", rcv_msg)
                            if (addr not in clientList):
                                clientList.append(addr)
                    except socket.error:
                        pass
                    current_time = int(round(time.time() * 1000))
                break
            # list of active clients
            print("Active clients", clientList)
            if len(clientList) > 1:
                break

        print("Client listening to mutlicast group is increasing.")
        for i in range(length):
            print("Sending file data to multicast group", fileData[i])
            sent = server.sendto(fileData[i], multicast_group)
            msg_sent_time = int(round(time.time() * 1000))
            current_time = int(round(time.time() * 1000))
            clientList = []

            while True:
                    while(current_time - msg_sent_time <= Timer ):
                        server.setblocking(False);
                        try:
                            data, addr = server.recvfrom(255)
                            if data != None:
                                rcv_msg = data.decode("utf-8")
                                print("Message from client: ", rcv_msg)
                                if(addr not in clientList):
                                    clientList.append(addr)
                        except socket.error:
                            pass
                        current_time= int(round(time.time() * 1000))
                    break
            # list of active clients
            print("Active clients", clientList)
            del clientList[0:len(clientList)]

    except Exception as err:
                log.info(err)

def udp_client_socket(mcast,client):
    ACK ='Ack'
    try:
        #create socket
        print("Create socket")
        client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        #bind to server address
        print("Binding to server address")
        client.bind(('', PORT))

        # add the socket to multicast group on all interfaces
        print("Adding the socket to multicast group on all interfaces")
        group = socket.inet_aton(mcast)
        mreq = struct.pack('=4sl', group, socket.INADDR_ANY)
        client.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

        while True:
            # receive data from
            print("Receive message")
            client.setblocking(True);
            try:
                data,addr= client.recvfrom(255)
                rcv_msg = data.decode("utf-8")
                print("Message from Server: ", rcv_msg)
                if rcv_msg == message.get("GOODBYE"):
                    break
            except socket.error:
                pass
            print("Send acknowledgement Ack")
            client.sendto(ACK.encode("utf-8"), addr)
        client.close()
    except Exception as err:
        log.info(err)












