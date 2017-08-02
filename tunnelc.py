#! /usr/bin/env python3

import sys
import socket


def LOG(*args, **kw):
    print(*args)


def ERROR(*args, **kw):
    print(*args)
    sys.exit()


def client(remote_ip, port=8080):
    try:
        # create an AF_INET, STREAM socket (TCP)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as e:
        ERROR('Failed to create socket')

    s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    LOG('Socket Create')

    # Connect to remote server
    try:
        s.connect((remote_ip, port))
    except socket.error as e:
        ERROR(e)
    data = s.recv(4096)

    print(data.decode())

    while True:
        i = input()
        print("input data: ", i)
        s.sendall(i.encode())
        data = s.recv(4096)
        print(data.decode())



if __name__ == "__main__":
    client('127.0.0.1')
