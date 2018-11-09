'''*************************************************************
  netster SOURCE FILE - Nischith Nanjundaswamy (nischith.cnn@gmail.com)
  CREATED: 11/8/2018
  This code provide Server and Client socket functionality with multicast
*************************************************************'''

import os
import time
import argparse
import socket
import logging as log

# Importing the assignment module a2.
from a4 import *

DEFAULT_PORT=2196

# This Server fucntion accepts host, protocol and port as the argument
# host is the Server IP, protocl is UDP/TCP and port is the Default port 12345'''
def run_server(mcast,f):
    log.info("Hello, I am a server...!!")
    udp_server_socket(mcast, f)

# This Client fucntion accepts host and port as the argument
# host is the Server IP and port is the Default port 12345'''
def run_client(mcast,client):
    log.info("Hello, I am a client...!!")
    udp_client_socket(mcast,client)


def main():
    parser = argparse.ArgumentParser(description="SICE Network netster")
    parser.add_argument('-p', '--port', type=str, default=DEFAULT_PORT,
                        help='listen on/connect to port <port> (default={}'
                        .format(DEFAULT_PORT))
    parser.add_argument('-i', '--iface', type=str, default='0.0.0.0',
                        help='listen on interface <dev>')
    parser.add_argument('-f', '--file', type=str,
                        help='file to read/write')
    parser.add_argument('-u', '--udp', action='store_true',
                        help='use UDP (default TCP)')
    parser.add_argument('-r', '--rudp', type=int, default=0,
                        help='use RUDP (1=stopwait, 2=gobackN)')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Produce verbose output')
    parser.add_argument('-m', '--mcast', type=str, default='226.0.0.1',
                        help='use multicast with specified group address')
    parser.add_argument('host', metavar='host', type=str, nargs='?',
                        help='connect to server at <host>')
    parser.add_argument('-c', '--client', type=str, default=0,
                        help='set to run as client')

    args = parser.parse_args()
    print(args)
    # configure logging level based on verbose arg
    level = log.DEBUG if args.verbose else log.INFO

    f = None
     # open the file if specified
    if args.file:
        try:
            mode = "rb"
            f = open(args.file, mode)
        except Exception as e:
            print("Could not open file: {}".format(e))
            exit(1)

    # Here we determine if we are a client or a server depending
    # on the presence of a "client" argument.
    if args.client:
        log.basicConfig(format='%(levelname)s:client: %(message)s',
                        level=level)
        run_client(args.mcast,args.client)
    else:
        log.basicConfig(format='%(levelname)s:server: %(message)s',
                        level=level)
        run_server(args.mcast, f)

if __name__ == "__main__":
    main()


