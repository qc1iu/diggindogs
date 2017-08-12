#! /usr/bin/env python3

import argparse
import select
import os
import struct
import fcntl
import binascii
import sys
import socket

TUNSETIFF = 0x400454ca
IFF_TAP = 0x0002
IFF_TUN = 0x0001
IFF_NO_PI = 0x1000
BUFSIZE = 2000

# some common lengths
IP_HDR_LEN = 20
ETH_HDR_LEN = 14
ARP_PKT_LEN = 28


def do_args():
    parser = argparse.ArgumentParser(description="simpletun!!")
    parser.add_argument('-i', '--ifacename', type=str, default="tun0")
    parser.add_argument('-s', '--server', action="store_true")
    parser.add_argument('-c', '--client')
    parser.add_argument('-p', '--port', type=int, default=55555)
    parser.add_argument('-d', '--debug', action="store_true")

    return parser.parse_args()


def ERROR(*args, **kw):
    print("ERROR>", *args, **kw)
    sys.exit()


def DEBUG(*args, **kw):
    print(*args, **kw)


def LOG(*args, **kw):
    print(*args, **kw)


def create_tun(name, flags):
    """
    type : name string
    type : flags unsigned int IFF_TUN|IFF_NO_PI
    rtype : int
    """
    fd = os.open("/dev/net/tun", os.O_RDWR)
    if fd < 0:
        ERROR("Opening /dev/net/tun")

    ifreq = struct.pack("16sH", name.encode(), flags)
    ifs = fcntl.ioctl(fd, TUNSETIFF, ifreq)

    tname = ifs[:16].decode().strip("\x00")
    LOG("Create tun: ", tname, "fd = ", fd)
    # ioctl
    return fd


def recv_thread(f, t):
    """
    type f: socket
    type t: socket
    """
    while True:
        data = f.recv(4096)
        t.sendall(data)


def doit(is_server, remote_ip, debug, port=55555):
    net_fd = 0
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # client
    if is_server == False:
        s.connect((remote_ip, port))
        net_socket = s
    # server
    else:
        s.bind(('127.0.0.1', port))
        s.listen(5)

        conn, remote_addr = s.accept()
        LOG("[Server] Connected with "
            + remote_addr[0] + ':' + str(remote_addr[1]))
        net_socket = conn

    net_fd = net_socket.fileno()
    rlist = [net_fd, sys.stdin.fileno()]
    while True:
        r_list, w_list, x_list = select.select(rlist, [], [], None)
        for r in r_list:
            if r is sys.stdin.fileno():
                data = os.read(sys.stdin.fileno(), BUFSIZE)
                os.write(net_fd, data)
            else:
#                data = s.recv(4096)
                data = os.read(net_fd, BUFSIZE)
                os.write(sys.stdout.fileno(), data)


if __name__ == "__main__":
    args = do_args()
    print(args)
    # check arg
    if args.server and args.client != None:
        raise Exception("wrong args")
    if args.server == False and args.client == None:
        raise Exception("wrong args")

    doit(args.server, args.client, args.debug, args.port)
