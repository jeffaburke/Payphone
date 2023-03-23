#!/usr/bin/env python3

# start the program
# ask a user for an input command to the source
# send the command over in some encoded way
#   craft the packet
# wait for new command

from scapy.all import *
from scapy.layers.inet import IP, ICMP

target = "0.0.0.0"


def makeICMPPacket(command):
    global target
    toBeSent = IP(dst=target) / ICMP(type=0) / command
    send(toBeSent, verbose=False)


# start program
def main() -> None:
    from sys import argv

    global target
    target = argv[1]
    while 1:
        command_input = str(input("Command input >> "))
        makeICMPPacket(command_input)


if __name__ == "__main__":
    main()
