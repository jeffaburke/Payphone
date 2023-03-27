#!/usr/bin/env python3

# start the program
# ask a user for an input command to the source
# send the command over in some encoded way
#   craft the packet
# wait for new command

from scapy.all import send
from scapy.layers.inet import IP, ICMP, UDP
from scapy.layers.dns import DNS, DNSRR, DNSQR

target = "0.0.0.0"  # this is a default value
protocol = "ICMP"


def makeICMPPacket(command):
    global target
    toBeSent = IP(dst=target) / ICMP(type=8) / command
    send(toBeSent, verbose=False)


def makeDNSPacket(command):
    global target
    query = DNS(
        rd=1,
        qd=DNSQR(qname="example.com"),
        an=DNSRR(rrname="example.com", type="TXT", rdata=command),
    )
    toBeSent = IP(dst=target) / UDP(port=53) / query


# start program
def main() -> None:
    from sys import argv

    global target
    target = argv[1]
    while 1:
        command_input = str(input("Command input >> "))
        makeICMPPacket(command_input)
        if command_input == "kill":
            kill = input(
                "Sent kill via ICMP. Would you like to kill the server (y/N)? "
            )
            if kill.lower() == "y":
                return


if __name__ == "__main__":
    main()
