import socket, os

# TODO Implement ICMP first cause supposedly easier... supposedly
# TODO Later: implement DNS packet transfering with scapy, packet crafting
from scapy.all import *

SERVER = "127.0.0.1"
PORT = 8080


def main() -> None:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client.connect((SERVER, PORT))
    client.sendall("Client Connected".encode())
    path = os.path
    client.sendall(f"{path}:".encode())
    i = 0
    while True:
        data = client.recv(1024)
        if data == "quit":
            break
        i += 1
    client.close()


if __name__ == "__main__":
    main()
