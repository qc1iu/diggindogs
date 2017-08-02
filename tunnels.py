#! /usr/bin/env python3

import socket
import sys
import threading
from util import Trace

g_t = Trace(indent=2, level=3)


def recv_thread(f, t):
    while True:
        data = f.recv(4096)
        t.sendall(data)


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

    t1 = threading.Thread(target=recv_thread, args=(conn, conn2))
    t2 = threading.Thread(target=recv_thread, args=(conn2, conn))

    t1.start()
    t2.start()

    t1.join()
    t2.join()


if __name__ == '__main__':
    server()
