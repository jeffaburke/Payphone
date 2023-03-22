# Deprecated

import socket, os

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
        try:
            data = client.recv(1024)
            if data == "quit":
                break
            i += 1
        except KeyboardInterrupt:
            break
    client.close()


if __name__ == "__main__":
    main()
