#! /usr/bin/env python3

import socket
import sys


def ERROR(*args, **kw):
    print(*args, **kw)
    sys.exit()


def LOG(*args, **kw):
    print(*args)


def server():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except:
        ERROR("Failed to create socket")
    s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    LOG("Socket created")

    host = '127.0.0.1'
    port = 9090
    try:
        s.bind((host, port))
    except socket.error:
        ERROR('Bind failed.')

    # start listening on socket
    s.listen(10)
    LOG("Socket now listening")

    conn, addr = s.accept()
    LOG('Connected with ' + addr[0] + ':' + str(addr[1]))


    try:
        s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except:
        ERROR('Failed to create socket s2.')

    LOG('Socket created.')
    try:
        s2.bind(('127.0.0.1', 8080))
    except socket.error:
        ERROR('Bind failed.')

    # start listening on socket s2
    s2.listen(10)
    LOG("Socket s2 now listening.")
    conn2, addr2 = s2.accept()
    LOG('Connected with ' + addr2[0] + ':' + str(addr2[1]))

    while True:
        data = conn.recv(4096)
        LOG("recv data from conn1")
        LOG("[DATA]", data.decode())
        conn2.sendall(data)

        data2 = conn2.recv(4096)
        LOG("recv data from conn2")
        LOG("[DATA]", data2.decode())
        conn.sendall(data2)

if __name__ == '__main__':
    server()
