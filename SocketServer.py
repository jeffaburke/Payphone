# Deprecated

import socket
from SocketClientThread import SocketClientThread

LOCALHOST = "127.0.0.1"
PORT = 8080


def main() -> None:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((LOCALHOST, PORT))
    print("Server started")
    print("Waiting for client request..")
    while True:
        server.listen(1)
        clientsock, clientAddress = server.accept()
        newthread = SocketClientThread(clientAddress, clientsock)
        newthread.start()


if __name__ == "__main__":
    try:
        main()
    except Exception:
        print("Error")
