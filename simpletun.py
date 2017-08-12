# /usr/bin/env python3
import select
import threading
import termios
import os
import struct
import fcntl
import binascii
import sys

TUNSETIFF = 0x400454ca
IFF_TAP = 0x0002
IFF_TUN = 0x0001
IFF_NO_PI = 0x1000
BUFSIZE = 2000
CLIENT = 0
SERVER = 1
remote_ip = ''
PORT = 55555

# some common lengths
IP_HDR_LEN = 20
ETH_HDR_LEN = 14
ARP_PKT_LEN = 28


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
    LOG("Create tun: ", tname)
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


def doit():
    net_fd = 0
    net_socket = 0
    tun_fd = create_tun("tun0", IFF_TUN | IFF_NO_PI)

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except:
        ERROR("Failed to create socket")

    s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    # client
    if cliserv == CLIENT:
        try:
            s.connect((remote_ip, PORT))
        except:
            ERROR("Client connect to %s error" % remote_ip)
        net_socket = s
    # server
    else:
        try:
            s.bind(('127.0.0.1', PORT))
        except:
            ERROR("Bind failed.")

        s.lisent()

        conn, remote_addr = s.accept()
        LOG("[Server] Connected with "
            + remote_addr[0] + ':' + str(remote_addr[1]))
        net_socket = conn

    net_fd = net_socket.fileno()
    rlist = [net_fd tun_fd]
    while True:
        r_list, w_list, x_list = select(rlist, None, None, None)

        for r in r_list:
            if r is net_fd:

                plength = os.read(r, 4)
                plength = struct.unpack("i", plength)
                data = os.read(r, plength)

                nwrite = os.write(tun_fd, data)
                DEBUG("Written %d bytes to the tap interface" % nwrite)
            else:
                # write length
                data = os.read(r, BUFSIZE)
                nread = len(data)
                DEBUG("Read %d bytes from the tap interface\n" % nread)

                plength = struct.pack("i", nread)
                os.write(net_fd, plength)
                nwrite = os.write(net_fd, data)

                DEBUG("Written %d bytes to the network\n",  nwrite)

    os.close(tun_fd)


if __name__ == "__main__":
    doit()
