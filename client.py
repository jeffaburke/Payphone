import socket, os


SERVER = "127.0.0.1"
PORT = 8080
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER, PORT))
client.sendall("Client Connected".encode())
i = 0
while i < 1:
    data = client.recv(1024)
    if data == "quit":
        break
    path = os.path
    client.sendall(f"{path}:".encode())
    i += 1
client.close()
