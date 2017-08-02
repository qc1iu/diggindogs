#! /usr/bin/env python3

import socket
import sys
from util import Trace

g_t = Trace(indent=2, level=3)


def server():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except:
        g_t.error("Failed to create socket")
    s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    g_t.log("Socket created")

    host = '127.0.0.1'
    port = 9090
    try:
        s.bind((host, port))
    except socket.error:
        g_t.error('Bind failed.')

    # start listening on socket
    s.listen()
    g_t.log("Socket now listening")

    conn, addr = s.accept()
    g_t.log('Connected with ' + addr[0] + ':' + str(addr[1]))


    try:
        s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except:
        g_t.error('Failed to create socket s2.')

    g_t.log('Socket created.')
    try:
        s2.bind(('127.0.0.1', 8080))
    except socket.error:
        g_t.error('Bind failed.')

    # start listening on socket s2
    s2.listen()
    g_t.log("Socket s2 now listening.")
    conn2, addr2 = s2.accept()
    g_t.log('Connected with ' + addr2[0] + ':' + str(addr2[1]))

    conn2.sendall("welcome little doggie!\n\n\n".encode())
    data = conn.recv(4096)
    g_t.log("recv data:")
    g_t.log(data.decode())

    # send 'cd'
    conn.sendall("cd\n".encode())

    while True:
        d = ""
        while True:
            data = conn.recv(4096)
            data = data.decode()
            d += data
            # a dirty hack
            # changing it according to your shell
            # To solve the problem, we need a client runing in the INSIDE,
            # instead of using the re
            if data.endswith("00m$ "):
                break;

        g_t.log("recv data from conn1")
        g_t.log("[DATA]", d)
        g_t.log("send data to conn2.")
        conn2.sendall(d.encode())


        data2 = conn2.recv(4096)
        g_t.log("recv data from conn2")
        g_t.log("[DATA]", data2.decode())
        g_t.log("send data to conn1.")
        g_t.log(data2)
        conn.sendall(data2)

if __name__ == '__main__':
    server()
